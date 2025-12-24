# 📋 README.md – Copy-Paste Ready

# Local AI Factory

A laptop-local, Docker-orchestrated Retrieval-Augmented Generation (RAG) system that:

- Ingests documents from a watched folder
- Builds a local knowledge base using embeddings and a vector store
- Answers questions via a RAG API
- Produces daily executive briefs
- Logs every meaningful action with hash-chained evidence for auditability

This repo is the implementation of the **Local AI Factory** architecture.

---

## 1. Features

- **Local-first**
    - Runs on a macOS laptop with Docker and local models (via Ollama).
    - No cloud calls in the default path.
- **Evidence-by-default**
    - Every ingestion, index, query, answer, brief, and evaluation emits a structured event.
    - Events are stored in append-only JSONL files with a SHA-256 hash chain.
- **Modular services**
    - Ingestion, Indexer, RAG API, Evidence Logger, Brief generator, Eval harness, and UI are separate services.
- **Self-testing**
    - Evaluation runner calls the RAG API with golden questions and hallucination traps.
    - Results are logged as `EvaluationEvent`s.

---

## 2. Repository structure

```
local-ai-factory/
  [README.md](http://README.md)
  .gitignore
  .env.example
  docker-compose.yml
  config/
  services/
  scripts/
  tests/
  docs/
  data/              # gitignored; holds inbox, logs, briefs
```

Key directories:

- `config/` – YAML configs for models, RAG behavior, evaluation, and logging
- `services/` – Python services (evidence logger, ingestion, indexer, RAG API, briefs, eval, UI, shared `common/`)
- `scripts/` – Developer helper scripts (bootstrap, dev up/down, tests)
- `tests/` – Unit, integration, and evaluation tests
- `docs/` – Architecture and runbook documentation
- `data/` – Local volumes for inbox documents, evidence logs, and briefs

For more detail, see `docs/[repo-structure.md](http://repo-structure.md)`.

---

## 3. Prerequisites

- **macOS** (tested on Apple Silicon)
- **Docker Desktop** installed from [docker.com](http://docker.com)
- **Git** (via Xcode Command Line Tools or installer)
- **Ollama** installed from [ollama.com](http://ollama.com) (no Homebrew)

---

## 4. Getting started

### 4.1 Clone and bootstrap

```bash
git clone <your-repo-url> local-ai-factory
cd local-ai-factory

# Create data directories and .env
./scripts/[bootstrap.sh](http://bootstrap.sh)
```

This will create:

- `data/inbox/` – drop documents here
- `data/logs/` – evidence logs
- `data/briefs/` – daily briefs
- `.env` – from `.env.example` if not present

### 4.2 Start the stack

```bash
./scripts/[dev-up.sh](http://dev-up.sh)
```

This runs `docker-compose.yml`, starting:

- Postgres (`db`)
- Evidence Logger (`evidence-logger`)
- Ingestion stub (`ingestion`)
- RAG API stub (`rag-api`)
- Minimal UI (`ui`)

### 4.3 Smoke test

1. Drop a small markdown file into `data/inbox/`.
2. Watch logs for ingestion and evidence-logger containers.
3. Call the RAG stub:

```bash
curl -X POST http://localhost:8000/rag/query \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the Local AI Factory?"}'
```

You should see a stubbed answer and citations in the response, and `QueryEvent` / `AnswerEvent` records in `data/logs/evidence-*.jsonl`.

---

## 5. Configuration

Configuration lives under `config/`:

- `config/models.yaml` – model routing (chat, embedding, judge)
- `config/rag.yaml` – chunking, retrieval parameters, prompt behavior
- `config/eval.yaml` – evaluation suites and grading thresholds
- `config/logging.yaml` – logging format and levels

Environment variables (most prefixed with `FACTORY_`) are defined in `.env.example` and used by the services.

---

## 6. Services

All services run inside the Docker Compose network and use shared `services/common/` utilities.

- **Evidence Logger** (`services/evidence_logger`)
    - FastAPI app exposing `POST /events` and `/verify`.
    - Writes hash-chained JSONL evidence logs.
- **Ingestion** (`services/ingestion`)
    - Scans `data/inbox/` for `.md` / `.txt`.
    - Computes SHA-256 and emits `IngestionEvent`s.
- **Indexer** (`services/indexer`)
    - Stubbed initially; later will chunk, embed, and populate the vector store.
- **RAG API** (`services/rag`)
    - FastAPI app exposing `POST /rag/query`.
    - Stubbed answer in v0.1 but enforces final request/response schema and evidence logging.
- **Briefs** (`services/briefs`)
    - Stub that writes a daily brief file and emits `DailyBriefEvent`s.
- **Eval** (`services/eval`)
    - CLI-oriented for now, with evaluation logic in `tests/evaluation/run_[eval.py](http://eval.py)`.
- **UI** (`services/ui`)
    - Minimal FastAPI stub exposing `/healthz`.
    - Can be expanded into a dashboard or replaced by Open WebUI.

---

## 7. Tests and evaluation

Run all tests:

```bash
./scripts/[run-tests.sh](http://run-tests.sh)
```

This runs:

- Unit tests under `tests/unit/`
- Integration tests under `tests/integration/`
- Evaluation smoke tests via `tests/evaluation/run_[eval.py](http://eval.py)`

Evaluation cases live in `tests/evaluation/questions.yaml`. Each case specifies:

- `question`
- `expected_contains`
- `forbid_phrases`

The evaluation runner calls the RAG API, scores answers, emits `EvaluationEvent`s, and prints a JSON summary.

---

## 8. Roadmap (phased build)

The repo is structured to be built in vertical slices:

1. **Phase 1** – contracts and bootstrap (events, config, basic structure)
2. **Phase 2** – Evidence Logger service + hash chain
3. **Phase 3** – Ingestion stub wired to Evidence Logger
4. **Phase 4** – RAG API stub with full request/response contract
5. **Phase 5** – Evaluation runner v0 and seed question suite
6. **Phase 6** – Real RAG: Indexer, embeddings, retrieval
7. **Phase 7** – Daily briefs and upgraded evaluation service

Each phase keeps the system runnable and auditable while you increase fidelity.

---

## 9. Docs

See the `docs/` directory for more detailed design notes:

- `docs/[architecture.md](http://architecture.md)` – high-level architecture and data flows
- `docs/[repo-structure.md](http://repo-structure.md)` – detailed repo layout
- `docs/[rag-pipeline.md](http://rag-pipeline.md)` – models, embeddings, and RAG behavior
- `docs/[evidence-model.md](http://evidence-model.md)` – evidence event schemas and hash chaining
- `docs/[evaluation.md](http://evaluation.md)` – evaluation and self-testing design
- `docs/[runbook.md](http://runbook.md)` – laptop setup and day-to-day operations

```

```

