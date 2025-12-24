from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import List

import httpx
from pydantic import BaseSettings

from services.common.events import (
    IngestionEvent,
    IngestionPayload,
    make_event,
)


class Settings(BaseSettings):
    inbox_dir: Path = Path(os.getenv("INBOX_DIR", "data/inbox"))
    evidence_logger_url: str = os.getenv("EVIDENCE_LOGGER_URL", "http://evidence-logger:9000/events")
    service_name: str = "ingestion"

    class Config:
        env_prefix = "FACTORY_"  # FACTORY_INBOX_DIR, FACTORY_EVIDENCE_LOGGER_URL, ...


settings = Settings()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_files() -> List[Path]:
    settings.inbox_dir.mkdir(parents=True, exist_ok=True)
    return [
        p
        for p in settings.inbox_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".md", ".txt"}
    ]


def build_ingestion_event(path: Path) -> IngestionEvent:
    stat = path.stat()
    payload = IngestionPayload(
        file_path=str(path),
        size_bytes=stat.st_size,
        mime_type="text/markdown" if path.suffix.lower() == ".md" else "text/plain",
        sha256=_sha256_file(path),
        source_host=os.uname().nodename,
    )
    return IngestionEvent(event_type="ingestion", service=settings.service_name, payload=payload)


def send_events(events: List[IngestionEvent]) -> None:
    if not events:
        return

    batch = {"events": [{"data": make_event(ev, service=settings.service_name)} for ev in events]}

    with httpx.Client(timeout=10.0) as client:
        resp = client.post(settings.evidence_logger_url, json=batch)
        resp.raise_for_status()


def run_once() -> None:
    files = discover_files()
    events = [build_ingestion_event(p) for p in files]
    send_events(events)


if __name__ == "__main__":
    run_once()
  
