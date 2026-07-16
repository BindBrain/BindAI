from dataclasses import dataclass, field

from .tool_call import ToolCall
from .usage import TokenUsage


@dataclass(slots=True)
class ModelResponse:
    """
    Response returned by a model provider.
    """

    content: str

    usage: TokenUsage

    tool_calls: list[ToolCall] = field(default_factory=list)