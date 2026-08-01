from __future__ import annotations

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

        namespace = self._storage.setdefault(
            record.namespace,
            {},
        )

        namespace[record.key] = record

        return MemoryResult(
            success=True,
            value=record,
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

        return MemoryResult(
            success=record is not None,
            value=record,
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

            if metadata:
                record_metadata = record.metadata or {}

                matches = all(
                    record_metadata.get(key) == value
                    for key, value in metadata.items()
                )

                if not matches:
                    continue

            if query in str(record.value).lower():
                results.append(
                    record,
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

        return key in self._storage.get(
            namespace,
            {},
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