# 🧪 Evaluation & Self-Testing Plan – Local AI Factory (evaluation.md)

### Purpose

Define how the Local AI Factory tests itself: correctness, robustness, and regression behavior.

### Evaluation Dimensions

- **Basic Correctness:** does the answer match expected content from documents?
- **Citation Quality:** are citations present, relevant, and non‑hallucinated?
- **Abstention Behavior:** does the system refuse when evidence is missing?
- **Stability:** do answers remain consistent between runs given the same corpus?
- **Performance:** latency and resource usage within reasonable limits for laptop use.

### Test Suite Types

1. **Golden Q&A Set**
    - Curated set of questions with expected answer patterns.
    - Stored as YAML / JSON in `tests/evaluation/questions.yaml`.
2. **Hallucination Traps**
    - Questions deliberately outside the corpus.
    - Expected outcome: explain limitation and decline to answer.
3. **Stress & Edge Cases**
    - Very long documents.
    - Conflicting documents.
    - Ambiguous questions requiring clarification.
4. **Regression Tests**
    - Lock in behavior for critical prompts and flows.
    - Compare current answers against previous snapshots.

### Evaluation Workflow

1. Developer or scheduler triggers `eval` service (CLI or HTTP).
2. Evaluation service iterates test cases and calls RAG API.
3. For each answer:
    - Applies rule‑based checks (e.g., citations present, length constraints).
    - Optionally calls local judge model to grade answer quality.
    - Produces structured `evaluation_event` with scores, error codes, and diffs.
4. Evidence Logger appends all `evaluation_event`s with hash chaining.

### Output Artifacts

- Evaluation runs stored with:
    - `evaluation_run_id`
    - test case id
    - inputs and outputs
    - scores and pass/fail flags.
- Optionally render a daily or per‑run **Evaluation Summary** markdown file under `/data/briefs`.

### Next Step

When you are ready, we can define concrete evaluation case templates (e.g., PCI‑flavored prompts, Interacture‑style briefs) and store them in a dedicated child page for reuse across projects.

[📂 Evaluation Seed Suite – Local AI Factory](%F0%9F%A7%AA%20Evaluation%20&%20Self-Testing%20Plan%20%E2%80%93%20Local%20AI%20Factor/%F0%9F%93%82%20Evaluation%20Seed%20Suite%20%E2%80%93%20Local%20AI%20Factory%20f9e625f27f7a4318a89767233d4de67a.md)

