from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI


app = FastAPI(title="Local AI Factory - Minimal UI Stub")


@app.get("/healthz")
async def healthcheck() -> Dict[str, Any]:
    return {"status": "ok"}


# Real implementation would provide HTML/JS for a simple dashboard and
# delegate chat and query traffic to the rag-api service.
