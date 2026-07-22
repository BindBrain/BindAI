from enum import Enum


class AgentState(str, Enum):
    IDLE = "idle"

    RUNNING = "running"

    WAITING_FOR_TOOL = "waiting_for_tool"

    COMPLETED = "completed"

    FAILED = "failed"
