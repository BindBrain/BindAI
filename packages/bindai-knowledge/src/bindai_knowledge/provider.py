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
    ) -> KnowledgeResult:
        ...

    @abstractmethod
    def get(
        self,
        document_id: str,
    ) -> KnowledgeResult:
        ...

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> KnowledgeResult:
        ...

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> KnowledgeResult:
        ...

    @abstractmethod
    def clear(
        self,
    ) -> KnowledgeResult:
        ...