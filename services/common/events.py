from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


SCHEMA_VERSION = "1.0.0"


class BaseEvent(BaseModel):
    """Common fields for all evidence events."""

    schema_version: str = Field(default=SCHEMA_VERSION)
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    service: str  # e.g., "ingestion", "indexer", "rag-api", "eval", "briefs"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Dict[str, Any]

    class Config:
        extra = "forbid"


class IngestionPayload(BaseModel):
    file_path: str
    size_bytes: int
    mime_type: str
    sha256: str
    source_host: Optional[str] = None


class IngestionEvent(BaseEvent):
    event_type: Literal["ingestion"]
    payload: IngestionPayload


class IndexPayload(BaseModel):
    document_id: str
    num_chunks: int
    embedding_model: str
    status: Literal["success", "error"]
    error_message: Optional[str] = None


class IndexEvent(BaseEvent):
    event_type: Literal["index"]
    payload: IndexPayload


class QueryPayload(BaseModel):
    question: str
    filters: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    query_embedding_id: Optional[str] = None


class QueryEvent(BaseEvent):
    event_type: Literal["query"]
    payload: QueryPayload


class AnswerPayload(BaseModel):
    question: str
    answer: str
    citations: List[Dict[str, Any]]  # e.g., {"doc_id": "...", "chunk_id": "...", "score": 0.92}
    latency_ms: int
    model_name: str
    abstained: bool = False


class AnswerEvent(BaseEvent):
    event_type: Literal["answer"]
    payload: AnswerPayload


class DailyBriefPayload(BaseModel):
    brief_path: str
    num_items: int
    period_start: datetime
    period_end: datetime


class DailyBriefEvent(BaseEvent):
    event_type: Literal["daily_brief"]
    payload: DailyBriefPayload


class EvaluationPayload(BaseModel):
    evaluation_run_id: str
    test_case_id: str
    score: float
    passed: bool
    failure_reasons: List[str] = []


class EvaluationEvent(BaseEvent):
    event_type: Literal["evaluation"]
    payload: EvaluationPayload


def make_event(event: BaseEvent, *, service: str) -> Dict[str, Any]:
    """Set the service and return a JSON-serializable dict for logging.

    This is the only function other services should use to emit events.
    """
    event.service = service
    return event.model_dump()
  
