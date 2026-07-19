from __future__ import annotations

from .message import ConversationMessage

from bindai_core.model import (
    Message,
    MessageRole,
)


class Conversation:
    """
    Conversation history.

    Shared by every conversational agent.
    """

    def __init__(self):

        self._messages: list[
            ConversationMessage
        ] = []

    #
    # Add messages
    #

    def add_user(
        self,
        text: str,
    ):

        self._messages.append(

            ConversationMessage(

                role=MessageRole.USER,

                content=text,

            )

        )

    def add_assistant(
        self,
        text: str,
    ):

        self._messages.append(

            ConversationMessage(

                role=MessageRole.ASSISTANT,

                content=text,

            )

        )

    def add_system(
        self,
        text: str,
    ):

        self._messages.append(

            ConversationMessage(

                role=MessageRole.SYSTEM,

                content=text,

            )

        )

    #
    # Access
    #

    @property
    def messages(
        self,
    ) -> list[Message]:

        return [

            Message(

                role=item.role,

                content=item.content,

            )

            for item in self._messages

        ]

    def clear(
        self,
    ):

        self._messages.clear()

    def last(
        self,
    ) -> ConversationMessage | None:

        if not self._messages:

            return None

        return self._messages[-1]

    def __len__(
        self,
    ):

        return len(
            self._messages
        )

    def __iter__(
        self,
    ):

        return iter(
            self._messages
        )