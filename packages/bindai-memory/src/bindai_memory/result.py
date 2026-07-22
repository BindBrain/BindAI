from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class MemoryResult:
    """
    Result returned from memory operations.
    """

    success: bool = True

    value: Any = None

    error: str | None = None
