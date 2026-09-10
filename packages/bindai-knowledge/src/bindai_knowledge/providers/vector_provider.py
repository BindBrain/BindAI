from __future__ import annotations

from bindai_core.embeddings import EmbeddingProvider

from ..document import KnowledgeDocument
from ..result import KnowledgeResult
from ..similarity import cosine_similarity
from ..vector_store import VectorRecord
from .in_memory import InMemoryKnowledgeProvider


def _normalize_scores(
    scores: list[float],
) -> list[float]:
    if not scores:
        return []

    maximum = max(scores)

    if maximum <= 0:
        return [0.0 for _ in scores]

    return [score / maximum for score in scores]


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

        ranked: list[
            tuple[
                float,
                KnowledgeDocument,
            ]
        ] = []

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

        keyword = super().search_with_scores(
            query=query,
            limit=1000,
            filters=filters,
        )

        vector = self.search_with_scores(
            query=query,
            limit=1000,
            filters=filters,
        )

        keyword_scores = {document.id: score for score, document in keyword.value}

        vector_scores = {document.id: score for score, document in vector.value}

        keyword_normalized_values = _normalize_scores(list(keyword_scores.values()))

        vector_normalized_values = _normalize_scores(list(vector_scores.values()))

        normalized_keyword = dict(
            zip(
                keyword_scores,
                keyword_normalized_values,
            )
        )

        normalized_vector = dict(
            zip(
                vector_scores,
                vector_normalized_values,
            )
        )

        document_by_id = {document.id: document for _, document in keyword.value}

        document_by_id.update({document.id: document for _, document in vector.value})

        candidate_ids = set(document_by_id)

        ranked: list[
            tuple[
                float,
                KnowledgeDocument,
            ]
        ] = []

        for document_id in candidate_ids:
            keyword_score = normalized_keyword.get(
                document_id,
                0.0,
            )

            vector_score = normalized_vector.get(
                document_id,
                0.0,
            )

            score = keyword_score * 0.6 + vector_score * 0.4

            ranked.append(
                (
                    score,
                    document_by_id[document_id],
                )
            )

        ranked.sort(
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
