from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WorkflowSchedule:
    """
    Describes when a workflow should execute.
    """

    workflow_id: str

    next_run: datetime

    interval_seconds: int | None = None

    enabled: bool = True