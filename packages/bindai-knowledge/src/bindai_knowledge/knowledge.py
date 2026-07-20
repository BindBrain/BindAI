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

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> str:

        result = self.search(
            query,
            limit,
        )

        if (
            not result.success
            or not result.value
        ):
            return ""

        return "\n\n".join(
            document.content
            for document in result.value
        )

    def load(
        self,
        loader,
    ) -> int:

        documents = loader.load()

        for document in documents:

            self.add(
                document,
            )

        return len(
            documents,
        )