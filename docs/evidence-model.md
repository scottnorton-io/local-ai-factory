# 📜 Evidence Logger, Audit Log & Hash Chaining – Local AI Factory (evidence-model.md)

### Purpose

Design the evidence system that makes the Local AI Factory auditable: structured logs, hash chaining, and event schemas.

### Evidence Logging Model

- **Transport:** simple HTTP endpoint or local queue; JSON events only.
- **Storage:** append‑only JSONL files under `./data/logs/evidence-YYYY-MM-DD.jsonl`.
- **Hash Chain:** each record includes a `prev_hash` and `record_hash` over the full JSON content.

### Core Event Schema (Conceptual)

Common fields for all events:

- `event_id` – UUID.
- `event_type` – `ingestion`, `index`, `query`, `answer`, `daily_brief`, `evaluation`, etc.
- `timestamp` – ISO‑8601 with timezone.
- `service` – `ingestion`, `rag-api`, `eval`, etc.
- `payload` – type‑specific JSON object.
- `prev_hash` – hex string (SHA‑256 of previous record).
- `record_hash` – hex string (SHA‑256 over this record with `prev_hash`).

### Example Event Types (Conceptual Only)

- **Ingestion Event**
    - `file_path`, `size_bytes`, `mime_type`, `sha256`, `source_host`.
- **Index Event**
    - `document_id`, `num_chunks`, `embedding_model`, `status`.
- **Query Event**
    - `question`, `user_id` (optional), `filters`, `query_embedding_id`.
- **Answer Event**
    - `question`, `answer`, `citations`, `latency_ms`, `model_name`.
- **Daily Brief Event**
    - `brief_path`, `num_items`, `period_start`, `period_end`.
- **Evaluation Event**
    - `evaluation_run_id`, `test_case_id`, `score`, `pass`, `failure_reasons`.

### Hash Chaining

- Evidence Logger maintains `prev_hash` in memory as it appends records.
- On restart, it reads the last record from the newest log file to resume the chain.
- Verification tool can recompute hashes from the first record onward and ensure continuity.

### Evidence Viewer (Optional)

- Small CLI or web view that can:
    - Filter events by type, date, or document id.
    - Recompute hash chains and flag breaks.
    - Export a bounded subset of events as a shareable bundle.

### Next Step

When you are ready, we can draft a separate child page with **copy‑paste‑ready JSON Schemas** or Pydantic models for each event type, aligned with this conceptual design.

[🧱 Evidence Event Models – Local AI Factory](%F0%9F%93%9C%20Evidence%20Logger,%20Audit%20Log%20&%20Hash%20Chaining%20%E2%80%93%20Loc/%F0%9F%A7%B1%20Evidence%20Event%20Models%20%E2%80%93%20Local%20AI%20Factory%203eb13fd171cd4c89852646300de5d984.md)

[🪵 Evidence Logger Service Stub – Local AI Factory](%F0%9F%93%9C%20Evidence%20Logger,%20Audit%20Log%20&%20Hash%20Chaining%20%E2%80%93%20Loc/%F0%9F%AA%B5%20Evidence%20Logger%20Service%20Stub%20%E2%80%93%20Local%20AI%20Factory%20886517d96e4642728ab674c9ec215fc9.md)

[🔍 Evidence Viewer Contract – Local AI Factory](%F0%9F%93%9C%20Evidence%20Logger,%20Audit%20Log%20&%20Hash%20Chaining%20%E2%80%93%20Loc/%F0%9F%94%8D%20Evidence%20Viewer%20Contract%20%E2%80%93%20Local%20AI%20Factory%20820e7ff109a9483abccb0a3161230dfe.md)

