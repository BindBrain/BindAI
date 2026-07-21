from __future__ import annotations

from dataclasses import dataclass

from .role import Role


@dataclass(slots=True)
class Message:
    """
    Chat message.
    """

    role: Role
    content: str


class SystemMessage(Message):

    def __init__(
        self,
        content: str,
    ):
        super().__init__(
            Role.SYSTEM,
            content,
        )


class UserMessage(Message):

    def __init__(
        self,
        content: str,
    ):
        super().__init__(
            Role.USER,
            content,
        )


class AssistantMessage(Message):

    def __init__(
        self,
        content: str,
    ):
        super().__init__(
            Role.ASSISTANT,
            content,
        )


class ToolMessage(Message):

    def __init__(
        self,
        content: str,
    ):
        super().__init__(
            Role.TOOL,
            content,
        )