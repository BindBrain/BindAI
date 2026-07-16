from enum import Enum


class AgentState(str, Enum):

    IDLE = "idle"

    RUNNING = "running"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"