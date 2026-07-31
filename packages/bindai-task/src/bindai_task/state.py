from enum import StrEnum


class TaskState(StrEnum):
    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"
