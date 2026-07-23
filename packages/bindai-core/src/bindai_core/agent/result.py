from __future__ import annotations

from dataclasses import dataclass

from bindai_core.executable import ExecutionResult


@dataclass(slots=True)
class AgentResult(ExecutionResult):
    """
    Execution result returned by an Agent.

    Exists as a semantic subtype of ExecutionResult so future
    agent-specific metadata can be added without changing the
    executable contract.
    """

    pass
