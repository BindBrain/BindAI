from enum import StrEnum


class ApplicationState(StrEnum):
    CREATED = "created"

    INITIALIZED = "initialized"

    RUNNING = "running"

    STOPPED = "stopped"

    DISPOSED = "disposed"
