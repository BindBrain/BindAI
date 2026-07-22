from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExecutionResponse:
    """
    Represents the result of an execution pipeline.
    """

    result: Any

    metadata: dict[str, object] = field(default_factory=dict)
