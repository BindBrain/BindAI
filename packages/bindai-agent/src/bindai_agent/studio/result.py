from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StudioExecutionResult:
    """
    Structured result of a Studio graph execution.
    """

    status: str = "completed"

    outputs: dict[str, Any] = field(
        default_factory=dict
    )

    error: dict[str, Any] | None = None


    def set_output(
        self,
        node_id: str,
        value: Any,
    ) -> None:

        self.outputs[node_id] = value


    def fail(
        self,
        node_id: str,
        error: Exception,
    ) -> None:

        self.status = "failed"

        self.error = {
            "node_id": node_id,
            "type": type(error).__name__,
            "message": str(error),
        }
