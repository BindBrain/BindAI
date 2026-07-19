from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class KnowledgeResult:
    """
    Result returned from knowledge operations.
    """

    success: bool = True

    value: Any = None

    error: str | None = None