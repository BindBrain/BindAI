from enum import Enum


class WorkflowState(str, Enum):
    """
    High-level workflow execution state.
    """

    CREATED = "created"

    RUNNING = "running"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"