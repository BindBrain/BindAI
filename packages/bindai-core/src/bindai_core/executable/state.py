from enum import StrEnum


class ExecutionStatus(StrEnum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
