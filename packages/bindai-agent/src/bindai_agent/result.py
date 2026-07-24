from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from bindai_core.executable import ExecutionResult


@dataclass(slots=True)
class AgentResult(ExecutionResult):
    """
    Result returned after an agent execution.
    """

    success: bool

    output: Any = None

    error: str | None = None