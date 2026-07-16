from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolCall:
    """
    Represents a request from the model
    to execute a tool.
    """

    name: str

    arguments: dict[str, Any] = field(default_factory=dict)