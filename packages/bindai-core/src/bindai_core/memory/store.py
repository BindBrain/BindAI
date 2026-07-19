from __future__ import annotations

from bindai_core.model import Message

from .backend import MemoryBackend


class InMemoryBackend(MemoryBackend):
    """
    Default in-process backend.
    """

    def __init__(self):

        self._messages: list[Message] = []

    def save(
        self,
        messages: list[Message],
    ) -> None:

        self._messages = list(
            messages,
        )

    def load(
        self,
    ) -> list[Message]:

        return list(
            self._messages,
        )

    def clear(
        self,
    ) -> None:

        self._messages.clear()