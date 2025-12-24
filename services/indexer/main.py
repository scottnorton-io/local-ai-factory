from __future__ import annotations

from pathlib import Path

from services.common.events import IndexEvent, IndexPayload, IngestionEvent, make_event


def process_ingestion_event(ev: IngestionEvent) -> IndexEvent:
    # Placeholder: in real implementation you would read the file, chunk, embed, and persist.
    payload = IndexPayload(
        document_id=ev.payload.file_path,
        num_chunks=0,
        embedding_model="nomic-embed-text",
        status="success",
        error_message=None,
    )
    return IndexEvent(event_type="index", service="indexer", payload=payload)


if __name__ == "__main__":
    # Placeholder entrypoint for manual testing later.
    print("Indexer stub - no runtime behavior yet.")
  
