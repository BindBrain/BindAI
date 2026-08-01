from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)


@dataclass(slots=True)
class ExecutionState:
    """
    Shared mutable state for the
    execution pipeline.
    """

    #
    # Model
    #

    request: ModelRequest | None = None

    response: ModelResponse | None = None

    #
    # Tool execution
    #

    tool_calls: list[Any] = field(
        default_factory=list,
    )

    #
    # Runtime
    #

    current_step: str | None = None

    iterations: int = 0

    finished: bool = False

    cancelled: bool = False

    streaming: bool = False

    #
    # Errors
    #

    errors: list[str] = field(
        default_factory=list,
    )

    #
    # Scratchpad
    #

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )