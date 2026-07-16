from dataclasses import dataclass, field

from .message import Message

from bindai_core.tool import ToolDefinition


@dataclass(slots=True)
class ModelRequest:
    """
    Request sent to a model provider.
    """

    messages: list[Message] = field(default_factory=list)

    temperature: float = 0.7

    tools: list[ToolDefinition] = field(default_factory=list)

    max_tokens: int | None = None

    top_p: float | None = None

    frequency_penalty: float | None = None

    presence_penalty: float | None = None

    stop: list[str] | None = None

    stream: bool = False

    