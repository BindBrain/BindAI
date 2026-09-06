from __future__ import annotations

from .document import KnowledgeDocument
from .provider import KnowledgeProvider
from .result import KnowledgeResult
from .search_options import KnowledgeSearchOptions


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

    def add_many(
        self,
        documents: list[KnowledgeDocument],
    ) -> KnowledgeResult:

        return self.provider.add_many(
            documents,
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
        filters: dict[str, object] | None = None,
        options: KnowledgeSearchOptions | None = None,
    ):
        """
        Search the knowledge base.

        Existing API remains supported while allowing
        future search options.
        """

        if options is None:
            options = KnowledgeSearchOptions(
                limit=limit,
                filters=filters,
            )

        return self.provider.search(
            query=query,
            limit=options.limit,
            filters=options.filters,
        )

    def search_with_scores(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ):
        return self.provider.search_with_scores(
            query,
            limit,
            filters,
        )

    def hybrid_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        return self.provider.hybrid_search(
            query=query,
            limit=limit,
            filters=filters,
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

        if not result.success or not result.value:
            return ""

        return "\n\n".join(document.content for document in result.value)

    def retrieve_with_sources(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        result = self.search(
            query,
            limit,
        )

        if not result.success or not result.value:
            return []

        return [
            {
                "citation": f"[{index}]",
                "id": document.id,
                "title": document.title,
                "content": document.content,
                "metadata": document.metadata,
            }
            for index, document in enumerate(result.value, start=1)
        ]

    def load(
        self,
        loader,
        chunker=None,
    ) -> int:

        documents = loader.load()

        count = 0

        for document in documents:
            if chunker is None:
                self.add(document)

                count += 1

            else:
                chunks = chunker.chunk(document)

                for chunk in chunks:
                    self.add(
                        KnowledgeDocument(
                            id=chunk.id,
                            title=document.title,
                            content=chunk.content,
                            metadata={
                                **(document.metadata or {}),
                                "document_id": document.id,
                                "chunk": True,
                            },
                        )
                    )

                    count += 1

        return count
