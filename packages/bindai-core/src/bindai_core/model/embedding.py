from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EmbeddingResponse:
    """
    Embedding generation result.
    """

    embedding: list[float]

    model: str

    dimensions: int
