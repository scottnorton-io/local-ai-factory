from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Chunk:
    text: str
    document_id: str
    index: int


def chunk_text(text: str, *, document_id: str = "", max_chars: int = 4000, min_chars: int = 200) -> Iterable[Chunk]:
    """Very simple size-based chunker placeholder.

    Real implementation should be header-aware and token-based; this version
    ensures you have a usable interface for early RAG experiments.
    """

    paragraphs: List[str] = [p.strip() for p in text.split("\n\n") if p.strip()]
    buf: List[str] = []
    buf_len = 0
    idx = 0

    for p in paragraphs:
        if buf_len + len(p) + 2 > max_chars and buf_len >= min_chars:
            yield Chunk(text="\n\n".join(buf), document_id=document_id, index=idx)
            idx += 1
            buf = [p]
            buf_len = len(p)
        else:
            buf.append(p)
            buf_len += len(p) + 2

    if buf:
        yield Chunk(text="\n\n".join(buf), document_id=document_id, index=idx)
      
