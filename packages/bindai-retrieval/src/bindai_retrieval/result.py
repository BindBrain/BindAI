from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalResult:
    """
    Result returned from retrieval.
    """

    success: bool

    documents: list

    error: str | None = None