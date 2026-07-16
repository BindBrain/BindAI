from __future__ import annotations

from dataclasses import dataclass, field

from bindai_core.context import ExecutionContext


@dataclass(slots=True)
class ExecutionRequest:
    """
    Represents a request sent to the execution pipeline.
    """

    agent: object

    context: ExecutionContext

    stream: bool = False

    metadata: dict[str, object] = field(default_factory=dict)