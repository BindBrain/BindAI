from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AgentResult:
    """
    Result returned after an agent execution.
    """

    success: bool

    output: Any = None

    error: str | None = None
