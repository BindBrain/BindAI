from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class WorkflowResult:
    """
    Result returned by WorkflowExecutor.
    """

    success: bool

    output: Any = None

    error: str | None = None