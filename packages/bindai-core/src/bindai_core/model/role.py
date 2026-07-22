from __future__ import annotations

from enum import Enum


class MessageRole(str, Enum):
    """
    Standard conversation roles.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

    TOOL = "tool"
