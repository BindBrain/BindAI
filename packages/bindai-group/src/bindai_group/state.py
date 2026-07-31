from __future__ import annotations

from enum import StrEnum


class GroupState(StrEnum):
    """
    Current execution state of a Group.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"
