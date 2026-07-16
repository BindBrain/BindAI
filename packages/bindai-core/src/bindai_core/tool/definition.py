from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolDefinition:
    """
    Serializable description of a tool.

    Providers consume ToolDefinition instead
    of the Tool instance itself.
    """

    name: str

    description: str

    parameters: dict[str, Any] = field(default_factory=dict)