from __future__ import annotations

import math
from datetime import UTC, datetime

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

        now = datetime.now(
            UTC,
        )

        if record.created_at is None:
            record.created_at = now

        record.updated_at = now

        record.embedding = self.embedding.embed(
            str(record.value),
        )

        self.records = [
            existing
            for existing in self.records
            if not (existing.key == record.key and existing.namespace == record.namespace)
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
            if record.key == key and record.namespace == namespace:
                if self._expired(
                    record,
                ):
                    continue

                record.last_accessed = datetime.now(
                    UTC,
                )

                record.access_count += 1

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
            if not (record.key == key and record.namespace == namespace)
        ]

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        return any(record.key == key and record.namespace == namespace for record in self.records)

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        self.records = [record for record in self.records if record.namespace != namespace]

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

            if self._expired(
                record,
            ):
                continue

            if metadata:
                matches = all(record.metadata.get(key) == value for key, value in metadata.items())

                if not matches:
                    continue

            if not record.embedding:
                continue

            semantic_score = self._cosine(
                query_embedding,
                record.embedding,
            )

            importance_bonus = record.importance * 0.10

            usage_bonus = min(
                record.access_count * 0.01,
                0.10,
            )

            decay_penalty = 0.0

            if record.last_accessed is not None:
                age_days = (
                    datetime.now(
                        UTC,
                    )
                    - record.last_accessed
                ).days

                decay_penalty = min(
                    age_days * 0.002,
                    0.10,
                )

            score = semantic_score + importance_bonus + usage_bonus - decay_penalty

            record.last_accessed = datetime.now(
                UTC,
            )

            record.access_count += 1

            result = MemoryRecord(
                key=record.key,
                value=record.value,
                namespace=record.namespace,
                type=record.type,
                metadata=record.metadata.copy(),
                importance=record.importance,
                access_count=record.access_count,
                created_at=record.created_at,
                updated_at=record.updated_at,
                last_accessed=record.last_accessed,
                expires_at=record.expires_at,
                embedding=record.embedding,
                score=score,
            )

            scored.append(
                result,
            )

        scored.sort(
            key=lambda record: record.score if record.score is not None else 0.0,
            reverse=True,
        )

        return scored[:limit]

    def _expired(
        self,
        record: MemoryRecord,
    ) -> bool:

        if record.expires_at is None:
            return False

        return (
            datetime.now(
                UTC,
            )
            >= record.expires_at
        )

    def _cosine(
        self,
        a: list[float],
        b: list[float],
    ) -> float:

        dot = sum(x * y for x, y in zip(a, b))

        na = math.sqrt(sum(x * x for x in a))

        nb = math.sqrt(sum(x * x for x in b))

        if na == 0 or nb == 0:
            return 0.0

        return dot / (na * nb)
