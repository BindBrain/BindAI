from __future__ import annotations

from abc import ABC, abstractmethod

from .document import KnowledgeDocument


class Reranker(ABC):
    """
    Base interface for knowledge document rerankers.
    """

    @abstractmethod
    def rerank(
        self,
        query: str,
        documents: list[KnowledgeDocument],
    ) -> list[KnowledgeDocument]:
        ...