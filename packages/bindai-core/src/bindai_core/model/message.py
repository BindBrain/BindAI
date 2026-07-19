from __future__ import annotations

from dataclasses import dataclass, field

from .role import MessageRole
from .tool_call import ToolCall


@dataclass(slots=True)
class Message:
    """
    Provider-agnostic conversation message.
    """

    role: MessageRole

    content: str = ""

    #
    # Tool response
    #

    tool_call_id: str | None = None

    #
    # Assistant tool requests
    #

    tool_calls: list[ToolCall] = field(
        default_factory=list,
    )

    #
    # Vision models
    #

    images: list[str] = field(
        default_factory=list,
    )