from __future__ import annotations

from dataclasses import dataclass

from bindai_core.executable import ExecutionResult


@dataclass(slots=True)
class AgentResult(ExecutionResult):
    """
    Result returned by an agent execution.
    """

    pass