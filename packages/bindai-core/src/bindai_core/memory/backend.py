from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.model import Message


class MemoryBackend(ABC):
    """
    Storage backend for chat memory.
    """

    @abstractmethod
    def save(
        self,
        messages: list[Message],
    ) -> None: ...

    @abstractmethod
    def load(
        self,
    ) -> list[Message]: ...

    @abstractmethod
    def clear(
        self,
    ) -> None: ...
