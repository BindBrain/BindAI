from __future__ import annotations

from enum import StrEnum


class MessageRole(StrEnum):
    """
    Standard conversation roles.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

    TOOL = "tool"
