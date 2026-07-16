from __future__ import annotations

from dataclasses import dataclass

from .tool_call import ToolCall
from .usage import TokenUsage


@dataclass(slots=True)
class ModelResponse:
    """
    Response returned by a model provider.
    """

    content: str

    usage: TokenUsage

    tool_call: ToolCall | None = None