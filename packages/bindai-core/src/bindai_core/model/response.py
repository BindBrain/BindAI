from dataclasses import dataclass, field
from typing import Any

from .tool_call import ToolCall
from .usage import TokenUsage


@dataclass(slots=True)
class ModelResponse:
    """
    Provider response.
    """

    content: str = ""

    tool_calls: list[ToolCall] = field(
        default_factory=list,
    )

    usage: TokenUsage = field(
        default_factory=TokenUsage,
    )

    finish_reason: str | None = None

    model: str | None = None

    structured_output: Any | None = None

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)