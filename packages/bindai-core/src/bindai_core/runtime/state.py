from enum import StrEnum


class RuntimeState(StrEnum):
    CREATED = "created"

    RUNNING = "running"

    STOPPED = "stopped"
