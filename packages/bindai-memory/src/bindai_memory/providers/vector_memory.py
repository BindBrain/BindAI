from __future__ import annotations

import math

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord
from bindai_memory.result import MemoryResult


class VectorMemoryProvider(MemoryProvider):
    def __init__(
        self,
        embedding: str = "random",
    ):

        from bindai_embeddings import EmbeddingRegistry

        self.embedding = EmbeddingRegistry.provider(
            embedding,
        )()

        self.records = []

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:

        record.embedding = self.embedding.embed(
            str(record.value),
        )

        self.records.append(
            record,
        )

        return MemoryResult(
            success=True,
            value=record,
        )

    def get(
        self,
        key: str,
        namespace: str = "default",
    ):

        for record in self.records:
            if record.key == key and record.namespace == namespace:
                return MemoryResult(
                    success=True,
                    value=record,
                )

        return MemoryResult(
            success=False,
        )

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ):

        self.records = [r for r in self.records if not (r.key == key and r.namespace == namespace)]

        return MemoryResult(success=True)

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ):

        return any(r.key == key and r.namespace == namespace for r in self.records)

    def clear(
        self,
        namespace: str = "default",
    ):

        self.records = [r for r in self.records if r.namespace != namespace]

        return MemoryResult(success=True)

    def search(
        self,
        query: str,
        namespace: str = "default",
        limit: int = 10,
        metadata=None,
    ):

        query_embedding = self.embedding.embed(query)

        scored = []

        for record in self.records:
            if record.namespace != namespace:
                continue

            score = self._cosine(
                query_embedding,
                record.embedding,
            )

            record.score = score

            scored.append(record)

        scored.sort(
            key=lambda r: r.score,
            reverse=True,
        )

        return scored[:limit]

    def _cosine(
        self,
        a,
        b,
    ):

        dot = sum(x * y for x, y in zip(a, b))

        na = math.sqrt(sum(x * x for x in a))

        nb = math.sqrt(sum(x * x for x in b))

        if na == 0 or nb == 0:
            return 0.0

        return dot / (na * nb)
