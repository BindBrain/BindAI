from __future__ import annotations

from ..document import KnowledgeDocument
from ..embedding import EmbeddingProvider
from ..result import KnowledgeResult
from ..similarity import cosine_similarity
from ..vector_store import VectorRecord
from ..embedding import EmbeddingProvider

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

        result = super().add(
            document,
        )

        self._vectors[
            document.id
        ] = VectorRecord(
            document=document,
            embedding=self.embedding.embed(
                document.content,
            ),
        )

        return result

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> KnowledgeResult:

        query_vector = self.embedding.embed(
            query,
        )

        ranked = []

        for record in self._vectors.values():

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
            key=lambda x: x[0],
        )

        return KnowledgeResult(
            success=True,
            value=[
                document
                for _, document in ranked[:limit]
            ],
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