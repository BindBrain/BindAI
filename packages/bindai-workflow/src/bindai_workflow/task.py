from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class HumanTask:
    """
    Represents a task waiting
    for a human.
    """

    id: str

    workflow_instance: str

    node_id: str

    assignee: str | None = None

    role: str | None = None

    created_at: datetime = datetime.utcnow()

    completed: bool = False

    result: str | None = None

    def approve(self):

        self.completed = True

        self.result = "approved"


    def reject(self):

        self.completed = True

        self.result = "rejected"