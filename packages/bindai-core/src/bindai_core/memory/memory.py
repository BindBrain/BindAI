from __future__ import annotations

from bindai_core.model import Message

from .backend import MemoryBackend
from .store import InMemoryBackend


class Memory:
    """
    Generic memory abstraction.
    """

    def __init__(
        self,
        backend: MemoryBackend | None = None,
    ):

        self.backend = backend or InMemoryBackend()

    def save(
        self,
        messages: list[Message],
    ) -> None:

        self.backend.save(
            messages,
        )

    def load(
        self,
    ) -> list[Message]:

        return self.backend.load()

    def clear(
        self,
    ) -> None:

        self.backend.clear()
