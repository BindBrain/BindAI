from dataclasses import dataclass
from enum import Enum
from typing import Any


class MemoryType(Enum):
    """
    Types of memory used by the AI system.
    """

    SHORT_TERM = "short_term"

    LONG_TERM = "long_term"

    WORKING = "working"

    SEMANTIC = "semantic"

    EPISODIC = "episodic"


@dataclass(slots=True)
class MemoryRecord:
    """
    Single memory record.
    """

    key: str

    value: Any

    namespace: str = "default"

    type: MemoryType = MemoryType.LONG_TERM

    metadata: dict[str, Any] | None = None
