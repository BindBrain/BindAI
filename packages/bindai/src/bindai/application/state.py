from enum import Enum


class ApplicationState(str, Enum):

    CREATED = "created"

    INITIALIZED = "initialized"

    RUNNING = "running"

    STOPPED = "stopped"

    DISPOSED = "disposed"