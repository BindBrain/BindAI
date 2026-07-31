from __future__ import annotations

from .provider import MemoryProvider
from .record import MemoryRecord
from .registry import MemoryRegistry
from .result import MemoryResult


class Memory:
    """
    High-level memory facade.
    """

    def __init__(
        self,
        provider: MemoryProvider | str | None = None,
    ):

        if provider is None:
            provider = "memory"

        if isinstance(
            provider,
            str,
        ):
            provider = (MemoryRegistry.provider(provider))()

        self.provider = provider

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:

        return self.provider.set(
            record,
        )

    def get(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        return self.provider.get(
            key,
            namespace,
        )

    def search(
        self,
        query: str,
        namespace: str = "default",
        limit: int = 10,
        metadata: dict | None = None,
    ):

        return self.provider.search(
            query=query,
            namespace=namespace,
            limit=limit,
            metadata=metadata,
        )

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        return self.provider.delete(
            key,
            namespace,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        return self.provider.exists(
            key,
            namespace,
        )

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        return self.provider.clear(
            namespace,
        )
