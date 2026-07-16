from __future__ import annotations

from bindai_core.model import (
    Message,
    MessageRole,
    ModelRequest,
)

from .message import ConversationMessage


class Conversation:
    """
    Stores the conversation exchanged between the user,
    assistant, system, tools, etc.
    """

    def __init__(self):

        self._messages: list[ConversationMessage] = []

    def add(
        self,
        role: MessageRole,
        content: str,
    ):

        self._messages.append(
            ConversationMessage(
                role=role,
                content=content,
            )
        )

    def add_system(
        self,
        content: str,
    ):

        self.add(
            MessageRole.SYSTEM,
            content,
        )

    def add_user(
        self,
        content: str,
    ):

        self.add(
            MessageRole.USER,
            content,
        )

    def add_assistant(
        self,
        content: str,
    ):

        self.add(
            MessageRole.ASSISTANT,
            content,
        )

    @property
    def messages(self):

        return list(self._messages)

    def clear(self):

        self._messages.clear()

    def __len__(self):

        return len(self._messages)

    def to_messages(self):

        return [
            Message(
                role=message.role,
                content=message.content,
            )
            for message in self._messages
        ]

    def to_request(self):

        return ModelRequest(
            messages=self.to_messages(),
        )