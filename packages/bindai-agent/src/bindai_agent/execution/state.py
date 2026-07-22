from __future__ import annotations

from dataclasses import dataclass

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)

from ..result import AgentResult


@dataclass(slots=True)
class ExecutionState:
    """
    Shared state used by the
    execution pipeline.
    """

    request: ModelRequest | None = None

    response: ModelResponse | None = None

    result: AgentResult | None = None

    finished: bool = False