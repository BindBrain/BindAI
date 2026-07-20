from __future__ import annotations

from bindai_core.model import (
    Message,
    MessageRole,
)


class Conversation:
    """
    Conversation history.

    Stores every message exchanged during an agent execution.
    """

    def __init__(self):

        self._messages: list[Message] = []

    #
    # Generic API
    #

    def add(
        self,
        message: Message,
    ) -> None:

        self._messages.append(
            message,
        )

    #
    # Convenience helpers
    #

    def add_user(
        self,
        text: str,
    ) -> None:

        self.add(

            Message(

                role=MessageRole.USER,

                content=text,

            )

        )

    def add_assistant(
        self,
        text: str,
        tool_calls=None,
    ):
        self.add(
            Message(
                role=MessageRole.ASSISTANT,
                content=text,
                tool_calls=tool_calls or [],
            )
        )

    def add_system(
        self,
        text: str,
    ) -> None:

        self.add(

            Message(

                role=MessageRole.SYSTEM,

                content=text,

            )

        )

    def add_tool(
        self,
        text: str,
        tool_call_id: str | None = None,
    ) -> None:

        self.add(

            Message(

                role=MessageRole.TOOL,

                content=text,

                tool_call_id=tool_call_id,

            )

        )

    #
    # Access
    #

    @property
    def messages(
        self,
    ) -> list[Message]:

        return list(
            self._messages,
        )

    def clear(
        self,
    ) -> None:

        self._messages.clear()

    def last(
        self,
    ) -> Message | None:

        if not self._messages:

            return None

        return self._messages[-1]

    def __len__(
        self,
    ):

        return len(self._messages)

    def __iter__(
        self,
    ):

        return iter(self._messages)