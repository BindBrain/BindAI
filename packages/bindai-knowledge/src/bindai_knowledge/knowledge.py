from __future__ import annotations

from .conversation_query import ConversationQuery
from .document import KnowledgeDocument
from .pipeline import KnowledgePipeline
from .provider import KnowledgeProvider
from .reranker_base import Reranker
from .result import KnowledgeResult
from .search_options import KnowledgeSearchOptions


class Knowledge:
    """
    High-level knowledge facade.
    """

    def __init__(
        self,
        provider: KnowledgeProvider,
        conversation_query: ConversationQuery | None = None,
        pipeline: KnowledgePipeline | None = None,
    ):
        self.provider = provider
        self.conversation_query = conversation_query or ConversationQuery()
        self.pipeline = pipeline or KnowledgePipeline()

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

    def search_conversation(
        self,
        conversation,
        limit: int = 5,
        filters: dict[str, object] | None = None,
        options: KnowledgeSearchOptions | None = None,
        reranker: Reranker | None = None,
    ):
        """
        Search the knowledge base using recent conversation history.
        """
        query = self.conversation_query.build(conversation)

        if not query:
            return KnowledgeResult(
                success=True,
                value=[],
            )

        return self.search(
            query=query,
            limit=limit,
            filters=filters,
            options=options,
            reranker=reranker,
        )

    def search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
        options: KnowledgeSearchOptions | None = None,
        reranker: Reranker | None = None,
    ):
        """
        Search the knowledge base.

        Existing API remains supported while allowing
        search type, minimum score, and optional reranking.
        """

        if options is None:
            options = KnowledgeSearchOptions(
                limit=limit,
                filters=filters,
            )

        if options.search_type == "vector":
            result = self.provider.search_with_scores(
                query=query,
                limit=options.limit,
                filters=options.filters,
            )
        elif options.search_type == "hybrid":
            result = self.provider.hybrid_search(
                query=query,
                limit=options.limit,
                filters=options.filters,
            )
        else:
            result = self.provider.search(
                query=query,
                limit=options.limit,
                filters=options.filters,
            )

        if options.min_score > 0 and result.success and result.value:
            scored_results = result.value

            if scored_results and isinstance(
                scored_results[0],
                tuple,
            ):
                result.value = [
                    document for score, document in scored_results if score >= options.min_score
                ]

        if reranker is not None and result.success and result.value:
            result.value = reranker.rerank(
                query,
                result.value,
            )

        return result

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
        reranker: Reranker | None = None,
    ) -> list[dict]:
        result = self.search(
            query,
            limit,
            reranker=reranker,
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
            for index, document in enumerate(
                result.value,
                start=1,
            )
        ]

    def load(
        self,
        loader,
        chunker=None,
    ) -> int:
        documents = loader.load()
        processed = self.pipeline.process(
            documents,
            chunker=chunker,
        )

        for document in processed:
            self.add(document)

        return len(processed)
