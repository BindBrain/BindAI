from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WorkflowEvent:
    """
    Base workflow event.
    """

    type: str

    timestamp: datetime

    workflow_id: str

    instance_id: str

    node_id: str | None = None

    workflow_version: int | None = None

@dataclass(slots=True)
class HumanTaskCreatedEvent(
    WorkflowEvent,
):
    pass


@dataclass(slots=True)
class HumanTaskCompletedEvent(
    WorkflowEvent,
):
    pass