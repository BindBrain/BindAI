from enum import Enum


class WorkflowState(str, Enum):

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"