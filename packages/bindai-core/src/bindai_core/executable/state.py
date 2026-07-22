from enum import Enum


class ExecutionStatus(str, Enum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
