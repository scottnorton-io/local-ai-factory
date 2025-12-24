from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BaseSettings, Field

from services.common.events import (
    AnswerEvent,
    AnswerPayload,
    QueryEvent,
    QueryPayload,
    make_event,
)


class Settings(BaseSettings):
    evidence_logger_url: str = Field(
        default="http://evidence-logger:9000/events",
        description="Evidence Logger /events endpoint",
    )
    service_name: str = "rag-api"

    class Config:
        env_prefix = "FACTORY_"  # FACTORY_EVIDENCE_LOGGER_URL, FACTORY_SERVICE_NAME


settings = Settings()
app = FastAPI(title="Local AI Factory - RAG API (Stub)")


class RAGQueryRequest(BaseModel):
    question: str
    filters: Optional[Dict[str, Any]] = None


class Citation(BaseModel):
    doc_id: str
    chunk_id: str
    score: float


class RAGQueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    meta: Dict[str, Any] = {}


def _emit_events(question: str, answer: str, citations: List[Citation], *, latency_ms: int) -> None:
    """Emit QueryEvent and AnswerEvent to the Evidence Logger."""

    query_payload = QueryPayload(question=question, filters=None, user_id=None, query_embedding_id=None)
    query_event = QueryEvent(event_type="query", service=settings.service_name, payload=query_payload)

    answer_payload = AnswerPayload(
        question=question,
        answer=answer,
        citations=[c.model_dump() for c in citations],
        latency_ms=latency_ms,
        model_name="stub-model",
        abstained=False,
    )
    answer_event = AnswerEvent(event_type="answer", service=settings.service_name, payload=answer_payload)

    batch = {
        "events": [
            {"data": make_event(query_event, service=settings.service_name)},
            {"data": make_event(answer_event, service=settings.service_name)},
        ]
    }

    with httpx.Client(timeout=5.0) as client:
        resp = client.post(settings.evidence_logger_url, json=batch)
        resp.raise_for_status()


@app.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(req: RAGQueryRequest) -> RAGQueryResponse:
    """Stub RAG endpoint.

    For Phase 4, returns a static answer with dummy citations but enforces the
    final contract and emits evidence events.
    """

    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty")

    start = datetime.utcnow()

    # Static answer for now; later phases will call real retrieval + LLM.
    answer = (
        "This is a stubbed RAG answer. The real implementation will retrieve "
        "supporting context from the vector store and generate an evidence-" 
        "backed response."
    )
    citations = [
        Citation(doc_id="stub-doc", chunk_id="stub-chunk", score=1.0),
    ]

    end = datetime.utcnow()
    latency_ms = int((end - start).total_seconds() * 1000)

    # Fire-and-forget; if logging fails, surface a 502 to callers so we do not
    # silently lose evidence.
    try:
        _emit_events(req.question, answer, citations, latency_ms=latency_ms)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Failed to log evidence: {exc}") from exc

    return RAGQueryResponse(
        answer=answer,
        citations=citations,
        meta={
            "latency_ms": latency_ms,
            "implementation": "stub",
        },
    )


@app.get("/healthz")
async def healthcheck() -> Dict[str, Any]:
    return {"status": "ok"}
  
