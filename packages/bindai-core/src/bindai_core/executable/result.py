from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExecutionResult:
    """
    Represents the outcome of executing any BindAI component.
    """

    success: bool
    output: Any = None
    error: str | None = None
