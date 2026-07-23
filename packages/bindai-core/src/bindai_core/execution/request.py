from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext

if TYPE_CHECKING:
    from bindai_core.executable import Executable


@dataclass(slots=True)
class ExecutionRequest:
    """
    Represents a request sent to the execution pipeline.
    """

    agent: Executable

    context: ExecutionContext

    stream: bool = False

    metadata: dict[str, object] = field(default_factory=dict)
