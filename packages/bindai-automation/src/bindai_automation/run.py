from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class AutomationRun:
    """
    Represents one execution of an automation definition.
    """

    definition_id: str
    definition_version: int
    id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "pending"
    input: Any = None
    output: Any = None
    error: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    started_at: datetime | None = None
    completed_at: datetime | None = None

    def start(self) -> None:
        self.status = "running"
        self.started_at = datetime.now(timezone.utc)

    def complete(self, output: Any = None) -> None:
        self.status = "completed"
        self.output = output
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, error: str) -> None:
        self.status = "failed"
        self.error = error
        self.completed_at = datetime.now(timezone.utc)