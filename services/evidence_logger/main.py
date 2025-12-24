from __future__ import annotations

import json
import os
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


LOG_DIR = Path(os.getenv("EVIDENCE_LOG_DIR", "data/logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Local AI Factory - Evidence Logger")


class EvidenceRecord(BaseModel):
    """Raw event record as received from other services.

    We intentionally accept a generic mapping here and do strict validation
    in the emitting services via `services/common/events.py`.
    """

    data: Dict[str, Any] = Field(..., description="Serialized event object")


class EvidenceBatch(BaseModel):
    events: List[EvidenceRecord]


_state: Dict[str, Optional[str]] = {
    "prev_hash": None,
}


def _log_path_for_date(ts: datetime) -> Path:
    day = ts.strftime("%Y-%m-%d")
    return LOG_DIR / f"evidence-{day}.jsonl"


def _init_prev_hash(ts: datetime) -> None:
    """Initialize `_state['prev_hash']` from the last line of today's file, if any."""

    if _state["prev_hash"] is not None:
        return

    path = _log_path_for_date(ts)
    if not path.exists():
        _state["prev_hash"] = None
        return

    last_line = None
    with path.open("rb") as f:
        # Seek from end to find last non-empty line
        f.seek(0, os.SEEK_END)
        pos = f.tell()
        buffer = bytearray()
        while pos > 0:
            pos -= 1
            f.seek(pos)
            char = f.read(1)
            if char == b"\n" and buffer:
                last_line = buffer[::-1].decode("utf-8")
                break
            buffer.extend(char)

    if not last_line:
        _state["prev_hash"] = None
        return

    try:
        record = json.loads(last_line)
        _state["prev_hash"] = record.get("record_hash")
    except json.JSONDecodeError:
        # If the last line is corrupt, we intentionally do not set prev_hash
        _state["prev_hash"] = None


def _append_event(raw_event: Dict[str, Any], *, ts: datetime) -> None:
    """Append a single event with hash chaining to today's log file."""

    _init_prev_hash(ts)

    prev_hash = _state["prev_hash"]

    envelope = {
        "timestamp": ts.isoformat(),
        "prev_hash": prev_hash,
        "event": raw_event,
    }

    # Compute record_hash over the canonical JSON representation of the envelope
    payload_bytes = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode("utf-8")
    record_hash = sha256(payload_bytes).hexdigest()
    envelope["record_hash"] = record_hash

    path = _log_path_for_date(ts)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(envelope, separators=(",", ":")))
        f.write("\n")

    _state["prev_hash"] = record_hash


@app.post("/events")
async def log_events(batch: EvidenceBatch) -> Dict[str, Any]:
    """Append one or more evidence events to the daily log.

    The expectation is that calling services already validated events
    using `services/common/events.py`. Here we focus on durability and
    hash chaining, not semantic validation.
    """

    if not batch.events:
        raise HTTPException(status_code=400, detail="No events provided")

    now = datetime.utcnow()

    for rec in batch.events:
        _append_event(rec.data, ts=now)

    return {"status": "ok", "count": len(batch.events)}


@app.get("/healthz")
async def healthcheck() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/verify")
async def verify(date: Optional[str] = None) -> Dict[str, Any]:
    """Verify the hash chain for a given day (YYYY-MM-DD).

    If `date` is omitted, verify today's file.
    """

    if date is None:
        ts = datetime.utcnow()
    else:
        try:
            ts = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

    path = _log_path_for_date(ts)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Log file not found for specified date")

    prev_hash: Optional[str] = None
    line_no = 0

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line_no += 1
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("prev_hash") != prev_hash:
                raise HTTPException(
                    status_code=500,
                    detail=f"Hash chain broken at line {line_no}",
                )

            payload_bytes = json.dumps(
                {k: record[k] for k in ("event", "prev_hash", "timestamp")},
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            expected_hash = sha256(payload_bytes).hexdigest()
            if record.get("record_hash") != expected_hash:
                raise HTTPException(
                    status_code=500,
                    detail=f"Record hash mismatch at line {line_no}",
                )

            prev_hash = record.get("record_hash")

    return {"status": "ok", "verified_lines": line_no}
  
