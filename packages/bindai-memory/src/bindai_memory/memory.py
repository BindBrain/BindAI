from __future__ import annotations

from bindai_memory.manager import MemoryManager

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
            provider = MemoryRegistry.provider(
                provider,
            )()

        self.provider = provider

        self.manager = MemoryManager()

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

        result = self.provider.get(
            key,
            namespace,
        )

        if result.success and result.value is not None:
            self.manager.touch(
                result.value,
            )

            self.manager.reinforce(
                result.value,
            )

            #
            # Persist updated lifecycle state
            #
            self.provider.set(
                result.value,
            )

            #
            # Return a fresh copy from storage
            #
            result = self.provider.get(
                key,
                namespace,
            )

        return result

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

    def close(
        self,
    ) -> None:
        """
        Close underlying provider if it supports closing.
        """

        close = getattr(
            self.provider,
            "close",
            None,
        )

        if callable(
            close,
        ):
            close()

    def __enter__(
        self,
    ):
        """
        Support context manager usage.
        """

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        """
        Automatically close provider.
        """

        self.close()
