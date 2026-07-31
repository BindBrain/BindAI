from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from bindai_core.schema import ResponseSchema

if TYPE_CHECKING:
    from bindai_core.tool.definition import ToolDefinition

from .message import Message


@dataclass(slots=True)
class ModelRequest:
    """
    Provider-agnostic model request.
    """

    messages: list[Message] = field(
        default_factory=list,
    )

    temperature: float | None = None

    max_tokens: int | None = None

    top_p: float | None = None

    frequency_penalty: float | None = None

    presence_penalty: float | None = None

    stop: list[str] | None = None

    stream: bool = False

    output_type: type | None = None

    tools: list[ToolDefinition] = field(
        default_factory=list,
    )

    response_schema: ResponseSchema | None = None
