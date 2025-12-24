import json
from uuid import UUID

from services.common.events import (
    AnswerEvent,
    AnswerPayload,
    BaseEvent,
    DailyBriefEvent,
    DailyBriefPayload,
    EvaluationEvent,
    EvaluationPayload,
    IngestionEvent,
    IngestionPayload,
    IndexEvent,
    IndexPayload,
    QueryEvent,
    QueryPayload,
)


def test_ingestion_event_round_trip() -> None:
    payload = IngestionPayload(
        file_path="data/inbox/sample.md",
        size_bytes=123,
        mime_type="text/markdown",
        sha256="abc123",
        source_host="test-host",
    )
    ev = IngestionEvent(event_type="ingestion", service="test", payload=payload)

    raw = ev.model_dump()
    as_json = json.dumps(raw)
    loaded = IngestionEvent.model_validate(json.loads(as_json))

    assert loaded.event_type == "ingestion"
    assert loaded.payload.file_path == payload.file_path


def test_index_event_status_and_error_message() -> None:
    payload = IndexPayload(
        document_id="doc-1",
        num_chunks=5,
        embedding_model="nomic-embed-text",
        status="error",
        error_message="failed to embed",
    )
    ev = IndexEvent(event_type="index", service="indexer", payload=payload)

    assert ev.payload.status == "error"
    assert ev.payload.error_message is not None


def test_query_and_answer_events_share_question_text() -> None:
    question = "What is the Local AI Factory?"
    q_payload = QueryPayload(question=question, filters=None, user_id=None, query_embedding_id=None)
    a_payload = AnswerPayload(
        question=question,
        answer="stub answer",
        citations=[],
        latency_ms=10,
        model_name="stub-model",
        abstained=False,
    )

    q_ev = QueryEvent(event_type="query", service="rag-api", payload=q_payload)
    a_ev = AnswerEvent(event_type="answer", service="rag-api", payload=a_payload)

    assert q_ev.payload.question == a_ev.payload.question


def test_daily_brief_event_has_period() -> None:
    from datetime import datetime, timedelta

    start = datetime.utcnow() - timedelta(days=1)
    end = datetime.utcnow()

    payload = DailyBriefPayload(
        brief_path="data/briefs/2025-12-24_daily_brief.md",
        num_items=3,
        period_start=start,
        period_end=end,
    )
    ev = DailyBriefEvent(event_type="daily_brief", service="briefs", payload=payload)

    assert ev.payload.period_end >= ev.payload.period_start


def test_evaluation_event_fields() -> None:
    payload = EvaluationPayload(
        evaluation_run_id="run-1",
        test_case_id="case-1",
        score=0.95,
        passed=True,
        failure_reasons=[],
    )
    ev = EvaluationEvent(event_type="evaluation", service="eval", payload=payload)

    assert isinstance(ev.event_id, UUID)
    assert ev.payload.passed is True
  
