from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ToolResult:
    """
    Result returned by every tool.
    """

    success: bool = True

    output: Any = None

    error: str | None = None