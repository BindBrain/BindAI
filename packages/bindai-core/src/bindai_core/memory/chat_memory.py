from __future__ import annotations

from bindai_core.model import Message


class ChatMemory:
    """
    Stores conversation messages.
    """

    def __init__(self):

        self._messages: list[Message] = []

    def add(
        self,
        message: Message,
    ):

        self._messages.append(message)

    def clear(self):

        self._messages.clear()

    def messages(self):

        return list(self._messages)