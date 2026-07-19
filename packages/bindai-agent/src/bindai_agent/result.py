from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AgentResult:
    """
    Result returned from agent execution.
    """

    success: bool
    output: str