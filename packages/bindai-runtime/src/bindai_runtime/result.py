from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ExecutionResult:
    success: bool

    value: Any = None

    error: Exception | None = None
