from __future__ import annotations

from bindai_core.conversation import Conversation
from bindai_core.model import (
    Message,
    MessageRole,
    ModelRequest,
)


class PromptBuilder:
    """
    Builds a ModelRequest from multiple sources.
    """

    def __init__(self):

        self._messages: list[Message] = []

    def system(
        self,
        content: str,
    ):

        self._messages.append(
            Message(
                role=MessageRole.SYSTEM,
                content=content,
            )
        )

        return self

    def user(
        self,
        content: str,
    ):

        self._messages.append(
            Message(
                role=MessageRole.USER,
                content=content,
            )
        )

        return self

    def assistant(
        self,
        content: str,
    ):

        self._messages.append(
            Message(
                role=MessageRole.ASSISTANT,
                content=content,
            )
        )

        return self

    def conversation(
        self,
        conversation: Conversation,
    ):

        self._messages.extend(
            conversation.to_messages()
        )

        return self

    def build(
        self,
    ) -> ModelRequest:

        return ModelRequest(
            messages=self._messages,
        )