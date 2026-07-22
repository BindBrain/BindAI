from __future__ import annotations

from bindai_core.model import (
    Message,
    MessageRole,
    ModelRequest,
)


class Conversation:
    """
    Stores the complete conversation history for an agent.
    """

    def __init__(self):

        self._messages: list[Message] = []

    def __len__(self) -> int:

        return len(self._messages)

    @property
    def messages(self) -> list[Message]:

        return self._messages

    def add_system(
        self,
        content: str,
    ) -> None:

        self._messages.append(
            Message(
                role=MessageRole.SYSTEM,
                content=content,
            )
        )

    def add_user(
        self,
        content: str,
    ) -> None:

        self._messages.append(
            Message(
                role=MessageRole.USER,
                content=content,
            )
        )

    def add_assistant(
        self,
        content: str,
    ) -> None:

        self._messages.append(
            Message(
                role=MessageRole.ASSISTANT,
                content=content,
            )
        )

    def add_assistant_tool_call(
        self,
        tool_calls: list,
    ) -> None:

        self._messages.append(
            Message(
                role=MessageRole.ASSISTANT,
                content="",
                tool_calls=tool_calls,
            )
        )

    def add_tool(
        self,
        *,
        tool_call_id: str,
        content: str,
    ) -> None:

        self._messages.append(
            Message(
                role=MessageRole.TOOL,
                content=content,
                tool_call_id=tool_call_id,
            )
        )

    def to_request(
        self,
    ) -> ModelRequest:

        request = ModelRequest()

        request.messages.extend(self._messages)

        return request
