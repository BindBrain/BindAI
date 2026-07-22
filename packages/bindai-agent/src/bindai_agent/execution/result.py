from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionResult:
    """
    Result returned by the execution engine.
    """

    success: bool

    response: str

    iterations: int = 0