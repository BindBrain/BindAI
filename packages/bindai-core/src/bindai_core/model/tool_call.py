from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolCall:
    """
    Tool invocation requested by the model.
    """

    id: str

    name: str

    arguments: dict[str, Any] = field(
        default_factory=dict,
    )
