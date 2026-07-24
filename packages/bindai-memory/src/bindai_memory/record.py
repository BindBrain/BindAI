from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MemoryType(Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    WORKING = "working"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"


@dataclass(slots=True)
class MemoryRecord:

    key: str

    value: Any

    namespace: str = "default"

    type: MemoryType = MemoryType.LONG_TERM

    metadata: dict[str, Any] = field(default_factory=dict)

    #
    # Semantic search
    #

    embedding: list[float] | None = None

    score: float | None = None