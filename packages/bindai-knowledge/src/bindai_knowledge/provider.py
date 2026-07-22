from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .document import KnowledgeDocument
from .result import KnowledgeResult


class KnowledgeProvider(ABC):
    """
    Base class for knowledge providers.
    """

    @abstractmethod
    def add(
        self,
        document: KnowledgeDocument,
    ) -> KnowledgeResult: ...

    @abstractmethod
    def add_many(
        self,
        documents: list[KnowledgeDocument],
    ) -> KnowledgeResult:

        results = []

        for document in documents:
            results.append(self.add(document))

        return KnowledgeResult(
            success=all(r.success for r in results),
            value=[r.value for r in results],
        )

    @abstractmethod
    def get(
        self,
        document_id: str,
    ) -> KnowledgeResult: ...

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult: ...

    @abstractmethod
    def search_with_scores(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult: ...

    @abstractmethod
    def hybrid_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult: ...

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> KnowledgeResult: ...

    @abstractmethod
    def clear(
        self,
    ) -> KnowledgeResult: ...
