from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ToolResult:
    """
    Result returned by a tool.
    """

    success: bool
    value: Any = None
    error: str | None = None
