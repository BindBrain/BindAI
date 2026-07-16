from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ToolResult:

    success: bool

    value: Any = None

    error: str | None = None

    @classmethod
    def ok(cls, value=None):
        return cls(
            success=True,
            value=value,
        )

    @classmethod
    def failed(cls, message: str):
        return cls(
            success=False,
            error=message,
        )