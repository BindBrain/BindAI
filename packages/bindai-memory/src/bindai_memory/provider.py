from __future__ import annotations

from abc import ABC, abstractmethod

from .record import MemoryRecord
from .result import MemoryResult


class MemoryProvider(ABC):
    """
    Base memory provider.
    """

    @abstractmethod
    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult: ...

    @abstractmethod
    def get(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult: ...

    @abstractmethod
    def search(
        self,
        query: str,
        namespace: str = "default",
        limit: int = 10,
        metadata: dict | None = None,
    ) -> list[MemoryRecord]: ...

    @abstractmethod
    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult: ...

    @abstractmethod
    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool: ...

    @abstractmethod
    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult: ...
