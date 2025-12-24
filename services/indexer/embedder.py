from __future__ import annotations

from typing import List

import httpx


class EmbeddingClient:
    def __init__(self, base_url: str = "http://host.docker.internal:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def embed(self, texts: List[str], model: str) -> List[List[float]]:
        # Placeholder for Ollama or other embedding provider.
        # Real implementation will depend on the model API you choose.
        raise NotImplementedError("EmbeddingClient.embed must be implemented for real RAG")
      
