# 🧠 Models, RAG & Indexing Pipeline – Local AI Factory (rag-pipeline.md)

### Purpose

Define local model choices, embedding strategy, and the RAG pipeline that turns raw documents into answerable, auditable knowledge.

### Model Strategy (Local‑First)

- **Default Chat / Generation Model**
    - Example: `llama3.1:8b` or `mistral:7b` in Ollama.
    - Role: answer generation, briefs, and evaluation summaries.
- **Embedding Model**
    - Example: `nomic-embed-text` or other high‑quality sentence embedding model in Ollama.
    - Role: document and query embeddings for vector search.
- **Optional Judge / Critic Model**
    - Can reuse the default model or pick a slightly larger one.
    - Role: grade answers during self‑test runs.

### Indexing Pipeline

1. **Document Normalization**
    - Convert PDF, DOCX, HTML, MD to a unified text representation.
    - Preserve key structure in metadata: headings, pages, sections, timestamps.
2. **Chunking**
    - Default strategy: ~500–1000 tokens per chunk with ~100–200 token overlap.
    - Consider header‑aware chunking where headings become chunk boundaries.
3. **Embedding**
    - For each chunk, call embedding endpoint and store:
        - vector
        - source document id
        - position (start_offset, end_offset)
        - content hash.
4. **Storage**
    - `documents` table: file‑level metadata (path, hash, type, tags).
    - `chunks` table: chunk text, embedding vector, references back to `documents`.
5. **Index Refresh / Rebuild**
    - Support incremental updates based on file hash changes.
    - Optionally support full rebuilds from scratch.

### Query‑Time RAG Flow

1. User asks a question via UI or API.
2. RAG Service embeds the question using the same embedding model.
3. Runs vector search against `chunks` with filters (e.g., `WHERE document.tag IN (...)`).
4. Ranks and truncates context to a token budget.
5. Builds a prompt with:
    - System message: role, constraints, and citation requirements.
    - Context: selected chunks with source ids.
    - User message: original question.
6. Calls generation model via Ollama.
7. Parses and returns structured answer + citation list.

### RAG Prompt Skeleton

You can keep this in `config/rag.yaml` as a template, but structurally:

- **System:** explain role as local knowledge operator, require citations and abstention when evidence is insufficient.
- **User (wrapped):** include question and context formatting instructions.
- **Output:** plain text answer plus a machine‑readable citations section (e.g., JSON or `DOC_ID:CHUNK_ID` list).

### Guardrails

- Require the model to **never hallucinate sources**: citations must map to actual chunk ids.
- Allow abstention: it is acceptable for the model to say it cannot answer from available evidence.
- Limit maximum answer length for predictability and readability.

### Next Step

Once model candidates are locked, you can add a child page with **model benchmarking notes** for your specific M3 Max host (latency vs. quality, context window behavior, etc.).

[🧾 RAG Prompt Contract – Local AI Factory](%F0%9F%A7%A0%20Models,%20RAG%20&%20Indexing%20Pipeline%20%E2%80%93%20Local%20AI%20Facto/%F0%9F%A7%BE%20RAG%20Prompt%20Contract%20%E2%80%93%20Local%20AI%20Factory%202dbc6e2f34b14038a08ab28bde311b4f.md)

[🧩 Local Model Matrix – M3 Max 64 GB (Local AI Factory)](%F0%9F%A7%A0%20Models,%20RAG%20&%20Indexing%20Pipeline%20%E2%80%93%20Local%20AI%20Facto/%F0%9F%A7%A9%20Local%20Model%20Matrix%20%E2%80%93%20M3%20Max%2064%20GB%20(Local%20AI%20Fact%20463060062df34f23afd9471cd7b476ff.md)

[📰 Daily Brief Prompt Contract – Local AI Factory](%F0%9F%A7%A0%20Models,%20RAG%20&%20Indexing%20Pipeline%20%E2%80%93%20Local%20AI%20Facto/%F0%9F%93%B0%20Daily%20Brief%20Prompt%20Contract%20%E2%80%93%20Local%20AI%20Factory%208612a5c3edeb4e6fafd502bb5f3afc92.md)

