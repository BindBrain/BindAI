from __future__ import annotations

from datetime import UTC, datetime

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord
from bindai_memory.result import MemoryResult


class InMemoryProvider(MemoryProvider):
    """
    Simple in-process memory provider.
    """

    def __init__(self):
        self._storage: dict[
            str,
            dict[str, MemoryRecord],
        ] = {}

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

        namespace = self._storage.setdefault(
            record.namespace,
            {},
        )

        namespace[record.key] = record

        return MemoryResult(
            success=True,
            value=self._clone(record),
        )

    def get(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        record = self._storage.get(
            namespace,
            {},
        ).get(
            key,
        )

        if record is None:
            return MemoryResult(
                success=False,
            )

        if self._expired(
            record,
        ):
            return MemoryResult(
                success=False,
            )

        return MemoryResult(
            success=True,
            value=self._clone(
                record,
            ),
        )

    def search(
        self,
        query: str,
        namespace: str = "default",
        limit: int = 10,
        metadata: dict | None = None,
    ) -> list[MemoryRecord]:

        if limit <= 0:
            return []

        query = query.lower()

        results: list[MemoryRecord] = []

        records = self._storage.get(
            namespace,
            {},
        ).values()

        for record in records:
            if self._expired(
                record,
            ):
                continue

            if metadata:
                matches = all(record.metadata.get(key) == value for key, value in metadata.items())

                if not matches:
                    continue

            if (
                query
                not in str(
                    record.value,
                ).lower()
            ):
                continue

            results.append(
                self._clone(
                    record,
                )
            )

            if len(results) >= limit:
                break

        return results

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        if namespace in self._storage:
            self._storage[namespace].pop(
                key,
                None,
            )

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        record = self._storage.get(
            namespace,
            {},
        ).get(
            key,
        )

        return record is not None and not self._expired(
            record,
        )

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        self._storage.pop(
            namespace,
            None,
        )

        return MemoryResult(
            success=True,
        )

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

    def _clone(
        self,
        record: MemoryRecord,
    ) -> MemoryRecord:

        return MemoryRecord(
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
            score=record.score,
        )
