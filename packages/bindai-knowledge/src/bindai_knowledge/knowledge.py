from __future__ import annotations

from .document import KnowledgeDocument
from .provider import KnowledgeProvider
from .result import KnowledgeResult


class Knowledge:
    """
    High-level knowledge facade.
    """

    def __init__(
        self,
        provider: KnowledgeProvider,
    ):

        self.provider = provider

    def add(
        self,
        document: KnowledgeDocument,
    ) -> KnowledgeResult:

        return self.provider.add(
            document,
        )

    def get(
        self,
        document_id: str,
    ) -> KnowledgeResult:

        return self.provider.get(
            document_id,
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> KnowledgeResult:

        return self.provider.search(
            query,
            limit,
        )

    def delete(
        self,
        document_id: str,
    ) -> KnowledgeResult:

        return self.provider.delete(
            document_id,
        )

    def clear(
        self,
    ) -> KnowledgeResult:

        return self.provider.clear()