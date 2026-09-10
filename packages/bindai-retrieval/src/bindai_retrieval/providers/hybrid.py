from __future__ import annotations

import math

from bindai_embeddings import EmbeddingRegistry
from bindai_knowledge import KnowledgeDocument

from ..provider import RetrieverProvider
from ..query import RetrievalQuery
from ..result import RetrievalResult
from .bm25 import BM25RetrieverProvider


class HybridRetrieverProvider(RetrieverProvider):
    def __init__(
        self,
        documents: list[KnowledgeDocument],
        embedding: str = "random",
    ):
        self.documents = documents

        self.bm25 = BM25RetrieverProvider(
            documents,
        )

        self.embedding = EmbeddingRegistry.provider(
            embedding,
        )()

        self._document_embeddings = {
            document.id: self.embedding.embed(
                f"{document.title} {document.content}",
            )
            for document in documents
        }

    def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:

        if not query.text.strip():
            return RetrievalResult(
                success=True,
                documents=[],
            )

        bm25_scores = self.bm25.score_documents(
            query,
        )

        bm25_by_id = {document.id: score for score, document in bm25_scores}

        maximum_bm25 = max(
            bm25_by_id.values(),
            default=0.0,
        )

        normalized_bm25 = {
            document_id: (score / maximum_bm25 if maximum_bm25 > 0 else 0.0)
            for document_id, score in bm25_by_id.items()
        }

        query_embedding = self.embedding.embed(
            query.text,
        )

        ranked: list[tuple[float, KnowledgeDocument]] = []

        for document in self.documents:
            if query.metadata:
                if not all(
                    document.metadata.get(key) == value for key, value in query.metadata.items()
                ):
                    continue

            document_embedding = self._document_embeddings.get(
                document.id,
            )

            if document_embedding is None:
                continue

            vector_score = self._cosine(
                query_embedding,
                document_embedding,
            )

            hybrid_score = (
                normalized_bm25.get(
                    document.id,
                    0.0,
                )
                * 0.6
                + vector_score * 0.4
            )

            ranked.append(
                (
                    hybrid_score,
                    document,
                )
            )

        ranked.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return RetrievalResult(
            success=True,
            documents=[document for _, document in ranked[: query.limit]],
        )

    @staticmethod
    def _cosine(
        a: list[float],
        b: list[float],
    ) -> float:

        dot = sum(x * y for x, y in zip(a, b))

        norm_a = math.sqrt(sum(x * x for x in a))

        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)
