from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class WorkflowDeployment:
    workflow_name: str

    version: int

    deployed_at: datetime
