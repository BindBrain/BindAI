from enum import StrEnum


class AgentState(StrEnum):
    IDLE = "idle"

    RUNNING = "running"

    WAITING_FOR_TOOL = "waiting_for_tool"

    COMPLETED = "completed"

    FAILED = "failed"
