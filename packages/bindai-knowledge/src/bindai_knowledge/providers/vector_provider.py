from __future__ import annotations

from ..document import KnowledgeDocument
from ..embedding import EmbeddingProvider
from ..result import KnowledgeResult
from ..similarity import cosine_similarity
from ..vector_store import VectorRecord
from .in_memory import InMemoryKnowledgeProvider


class VectorKnowledgeProvider(InMemoryKnowledgeProvider):
    def __init__(
        self,
        embedding: EmbeddingProvider,
    ):

        super().__init__()

        self.embedding = embedding

        self._vectors: dict[
            str,
            VectorRecord,
        ] = {}

    def add(
        self,
        document: KnowledgeDocument,
    ) -> KnowledgeResult:

        result = super().add(document)

        self._vectors[document.id] = VectorRecord(
            document=document,
            embedding=self.embedding.embed(
                document.content,
            ),
        )

        return result

    def add_many(
        self,
        documents: list[KnowledgeDocument],
    ) -> KnowledgeResult:

        for document in documents:
            self._documents[document.id] = document

            self._vectors[document.id] = VectorRecord(
                document=document,
                embedding=self.embedding.embed(
                    document.content,
                ),
            )

        return KnowledgeResult(
            success=True,
            value=documents,
        )

    def search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        result = self.search_with_scores(
            query=query,
            limit=limit,
            filters=filters,
        )

        return KnowledgeResult(
            success=result.success,
            value=[document for _, document in result.value],
        )

    def search_with_scores(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        query_vector = self.embedding.embed(
            query,
        )

        ranked: list[tuple[float, KnowledgeDocument]] = []

        for record in self._vectors.values():
            if filters:
                metadata = record.document.metadata or {}

                if not all(metadata.get(key) == value for key, value in filters.items()):
                    continue

            score = cosine_similarity(
                query_vector,
                record.embedding,
            )

            ranked.append(
                (
                    score,
                    record.document,
                )
            )

        ranked.sort(
            reverse=True,
            key=lambda item: item[0],
        )

        return KnowledgeResult(
            success=True,
            value=ranked[:limit],
        )

    def hybrid_search(
        self,
        query: str,
        limit: int = 5,
        filters: dict[str, object] | None = None,
    ) -> KnowledgeResult:

        #
        # Keyword ranking
        #

        keyword = super().search_with_scores(
            query=query,
            limit=1000,
            filters=filters,
        )

        #
        # Vector ranking
        #

        vector = self.search_with_scores(
            query=query,
            limit=1000,
            filters=filters,
        )

        #
        # Merge
        #

        merged: dict[
            str,
            tuple[
                float,
                KnowledgeDocument,
            ],
        ] = {}

        for score, document in keyword.value:
            merged[document.id] = (
                score * 0.4,
                document,
            )

        for score, document in vector.value:
            if document.id in merged:
                merged_score, _ = merged[document.id]

                merged[document.id] = (
                    merged_score + score * 0.6,
                    document,
                )

            else:
                merged[document.id] = (
                    score * 0.6,
                    document,
                )

        ranked = sorted(
            merged.values(),
            key=lambda item: item[0],
            reverse=True,
        )

        return KnowledgeResult(
            success=True,
            value=[document for _, document in ranked[:limit]],
        )

    def delete(
        self,
        document_id: str,
    ) -> KnowledgeResult:

        self._vectors.pop(
            document_id,
            None,
        )

        return super().delete(
            document_id,
        )

    def clear(
        self,
    ) -> KnowledgeResult:

        self._vectors.clear()

        return super().clear()
