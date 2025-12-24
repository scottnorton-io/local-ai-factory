# 📁 Repository & Directory Structure – Local AI Factory (repo-structure.md)

### Purpose

Define a repo layout that is easy to reason about on macOS, Docker‑first, and ready to export as a public GitHub project.

### Top‑Level Layout (Conceptual)

```
local-ai-factory/
  [README.md](http://README.md)
  LICENSE
  docker-compose.yml
  .env.example
  scripts/
  services/
  ui/
  tests/
  docs/
  data/
    inbox/
    briefs/
    logs/
  config/
```

### Directory Breakdown

- **README.md**
    - Top‑level overview, quickstart, and architecture links.
    - Includes how to get from zero → running factory in 5 minutes.
- **docker-compose.yml**
    - Declares all core services: db, vector store, ingestion, indexer, rag, eval, evidence logger, UI.
    - Uses named volumes and explicit port mappings.
- **.env.example**
    - Safe defaults (no secrets).
    - Variables for ports, model names, and feature flags.
- **scripts/**
    - `bootstrap.sh` – one‑time setup (volumes, permissions, sample data).
    - `dev-up.sh` / `dev-down.sh` – bring the stack up/down.
    - `run-tests.sh` – run unit + integration tests.
- **services/**
    - `ingestion/` – watches `/data/inbox`, normalizes documents, emits events.
    - `indexer/` – chunks text, calls embeddings, populates vector store.
    - `rag/` – HTTP API for query / answer.
    - `briefs/` – daily executive brief generator.
    - `eval/` – self‑test harness and evaluation logic.
    - `evidence-logger/` – append‑only JSONL log sink with hash chaining.
    - `common/` – shared libraries (logging, schema definitions, event clients).
- **ui/**
    - `web/` – optional minimal web UI if not using Open WebUI directly.
    - `open-webui-config/` – configuration, presets, and model routing docs.
- **tests/**
    - `unit/` – per‑service tests.
    - `integration/` – docker‑compose‑driven flows (ingest → query → log).
    - `evaluation/` – Q&A suites and expected patterns.
- **docs/**
    - Architecture diagrams, ADRs, and markdown guides.
    - Links back to the Notion documentation pages for deeper context.
- **data/** (bind‑mounted from host)
    - `inbox/` – drop‑in folder for raw files.
    - `briefs/` – rendered daily briefs.
    - `logs/` – evidence logs (JSONL) and service logs.
- **config/**
    - `models.yaml` – model routing and options.
    - `rag.yaml` – chunking and retrieval parameters.
    - `eval.yaml` – evaluation suite configuration.

### Suggested File‑Level Conventions

- Use **snake_case** for Python files and directories.
- Keep Dockerfiles in each `services/<name>/Dockerfile`.
- Keep service‑local configuration under `services/<name>/config/` when needed.
- Prefer relative imports within `services/` and share only stable contracts via `services/common/`.

### Next Step

Once you are ready, we can create a dedicated child page for **copy‑paste‑ready file stubs** (e.g., `docker-compose.yml`, example `Dockerfile`s, and main entrypoints) following your Nested Markdown prevention rules.

