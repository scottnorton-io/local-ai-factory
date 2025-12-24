# 🚀 Laptop Setup & Runbook – Local AI Factory (runbook.md)

### Purpose

Give you a short, repeatable path from zero → running Local AI Factory on a macOS M3 Max laptop, without Homebrew.

### Prerequisites (macOS)

- **Docker Desktop** installed from [docker.com](http://docker.com).
- **Git** via Xcode Command Line Tools or direct installer.
- **Ollama** installed from [[ollama.com](http://ollama.com)] (direct download; no Homebrew).

### One‑Time Setup

1. **Clone the repo** (or create `local-ai-factory/`).
2. Create directories:
    - `mkdir -p data/inbox data/briefs data/logs`.
3. Copy `.env.example` → `.env` and adjust ports/model names if needed.
4. Start Ollama and pull models:
    - `ollama pull <chat-model>`
    - `ollama pull <embedding-model>`

### Run the Stack

1. From the project root, start services:
    - `docker compose up -d` (or `scripts/dev-up.sh`).
2. Wait for:
    - `db`, `ingestion`, `indexer`, `rag-api`, `evidence-logger`, and `ui` to become healthy.
3. Open UI at `http://localhost:3000` (or the configured port).

### Smoke Test Flow

1. Drop a small markdown file into `data/inbox/` with a few bullet points.
2. Watch logs for `ingestion` and `indexer` containers.
3. In UI, ask a question that the document should answer.
4. Confirm:
    - Useful answer with citations.
    - Evidence log file created under `data/logs`.

### Daily Usage

- Drop new docs into `data/inbox/` as needed.
- Skim the Daily Executive Brief each morning in `data/briefs/`.
- Periodically run evaluation suite via the `eval` service.

### Tear‑Down

- Stop containers: `docker compose down`.
- Preserve `data/` for reuse; delete if you want a clean slate.

### Next Step

When you are ready to publish, this page can be mirrored into a GitHub‑ready `docs/runbook.md` with minor path tweaks and links to the repo’s README.

