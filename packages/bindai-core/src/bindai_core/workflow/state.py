from enum import StrEnum


class WorkflowState(StrEnum):
    """
    High-level workflow execution state.
    """

    CREATED = "created"

    RUNNING = "running"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"
