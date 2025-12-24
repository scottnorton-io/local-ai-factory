from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import httpx
import yaml

from services.common.events import EvaluationEvent, EvaluationPayload, make_event


@dataclass
class TestCase:
    id: str
    question: str
    expected_contains: List[str]
    forbid_phrases: List[str]


def load_cases(path: Path) -> List[TestCase]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    cases: List[TestCase] = []
    for item in data:
        cases.append(
            TestCase(
                id=item["id"],
                question=item["question"],
                expected_contains=item.get("expected_contains", []),
                forbid_phrases=item.get("forbid_phrases", []),
            )
        )
    return cases


def grade_answer(answer: str, case: TestCase) -> Dict[str, Any]:
    score = 1.0
    failures: List[str] = []

    for expected in case.expected_contains:
        if expected not in answer:
            failures.append(f"missing expected substring: {expected!r}")
            score -= 0.5 / max(1, len(case.expected_contains))

    for phrase in case.forbid_phrases:
        if phrase in answer:
            failures.append(f"forbidden phrase present: {phrase!r}")
            score -= 0.5 / max(1, len(case.forbid_phrases))

    score = max(0.0, min(1.0, score))
    return {"score": score, "failures": failures}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="smoke")
    parser.add_argument("--questions", default="tests/evaluation/questions.yaml")
    parser.add_argument("--rag-url", default="http://localhost:8000/rag/query")
    parser.add_argument("--evidence-logger-url", default="http://localhost:9000/events")
    args = parser.parse_args()

    cases = load_cases(Path(args.questions))

    results: List[Dict[str, Any]] = []

    with httpx.Client(timeout=15.0) as client:
        for case in cases:
            resp = client.post(args.rag_url, json={"question": case.question})
            resp.raise_for_status()
            body = resp.json()
            answer = body.get("answer", "")
            grade = grade_answer(answer, case)

            passed = grade["score"] >= 0.8 and not grade["failures"]

            results.append(
                {
                    "id": case.id,
                    "score": grade["score"],
                    "passed": passed,
                    "failures": grade["failures"],
                }
            )

    # Emit EvaluationEvent batch
    events = []
    for r in results:
        payload = EvaluationPayload(
            evaluation_run_id="local-run",
            test_case_id=r["id"],
            score=r["score"],
            passed=r["passed"],
            failure_reasons=r["failures"],
        )
        ev = EvaluationEvent(event_type="evaluation", service="eval", payload=payload)
        events.append({"data": make_event(ev, service="eval")})

    with httpx.Client(timeout=15.0) as client:
        if events:
            client.post(args.evidence_logger_url, json={"events": events}).raise_for_status()

    # Print a simple summary for CLI use
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
  
