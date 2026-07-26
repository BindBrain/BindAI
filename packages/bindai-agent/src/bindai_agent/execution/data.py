from __future__ import annotations

from dataclasses import dataclass

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)

from bindai_core.agent import AgentResult


@dataclass(slots=True)
class ExecutionData:
    """
    Runtime objects produced during
    execution.

    Unlike ExecutionState from
    bindai-core, this stores
    execution data rather than
    lifecycle state.
    """

    request: ModelRequest | None = None

    response: ModelResponse | None = None

    result: AgentResult | None = None
