from __future__ import annotations

from enum import Enum


class GroupState(str, Enum):
    """
    Current execution state of a Group.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"
