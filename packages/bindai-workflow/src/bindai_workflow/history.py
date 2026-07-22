from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WorkflowHistory:
    instance_id: str

    workflow_id: str

    workflow_version: int

    started_at: datetime

    finished_at: datetime | None

    success: bool

    error: str | None = None
