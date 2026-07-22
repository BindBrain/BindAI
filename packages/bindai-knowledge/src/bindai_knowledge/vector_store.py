from __future__ import annotations

from dataclasses import dataclass

from .document import KnowledgeDocument


@dataclass(slots=True)
class VectorRecord:
    document: KnowledgeDocument

    embedding: list[float]
