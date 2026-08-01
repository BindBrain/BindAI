from __future__ import annotations

from datetime import datetime, timezone
import math

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord
from bindai_memory.result import MemoryResult


class VectorMemoryProvider(MemoryProvider):
    """
    In-memory vector based memory provider.
    """

    def __init__(
        self,
        embedding: str = "random",
    ):

        from bindai_embeddings import EmbeddingRegistry

        self.embedding = EmbeddingRegistry.provider(
            embedding,
        )()

        self.records: list[MemoryRecord] = []

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:

        record.embedding = self.embedding.embed(
            str(record.value),
        )

        record.updated_at = datetime.now(
            timezone.utc,
        )

        self.records = [
            existing
            for existing in self.records
            if not (
                existing.key == record.key
                and existing.namespace == record.namespace
            )
        ]

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
    ) -> MemoryResult:

        for record in self.records:

            if (
                record.key == key
                and record.namespace == namespace
            ):

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
    ) -> MemoryResult:

        self.records = [
            record
            for record in self.records
            if not (
                record.key == key
                and record.namespace == namespace
            )
        ]

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        return any(
            record.key == key
            and record.namespace == namespace
            for record in self.records
        )

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        self.records = [
            record
            for record in self.records
            if record.namespace != namespace
        ]

        return MemoryResult(
            success=True,
        )

    def search(
        self,
        query: str,
        namespace: str = "default",
        limit: int = 10,
        metadata: dict | None = None,
    ) -> list[MemoryRecord]:

        query_embedding = self.embedding.embed(
            query,
        )

        scored: list[MemoryRecord] = []

        for record in self.records:

            if record.namespace != namespace:
                continue

            if metadata:

                matches = all(
                    record.metadata.get(key) == value
                    for key, value in metadata.items()
                )

                if not matches:
                    continue

            if not record.embedding:
                continue

            score = self._cosine(
                query_embedding,
                record.embedding,
            )

            result = MemoryRecord(
                key=record.key,
                value=record.value,
                namespace=record.namespace,
                type=record.type,
                metadata=record.metadata,
                embedding=record.embedding,
                score=score,
                created_at=record.created_at,
                updated_at=record.updated_at,
            )

            scored.append(
                result,
            )

        scored.sort(
            key=lambda record: (
                record.score
                if record.score is not None
                else 0.0
            ),
            reverse=True,
        )

        return scored[:limit]

    def _cosine(
        self,
        a: list[float],
        b: list[float],
    ) -> float:

        dot = sum(
            x * y
            for x, y in zip(a, b)
        )

        na = math.sqrt(
            sum(
                x * x
                for x in a
            )
        )

        nb = math.sqrt(
            sum(
                x * x
                for x in b
            )
        )

        if na == 0 or nb == 0:
            return 0.0

        return dot / (na * nb)