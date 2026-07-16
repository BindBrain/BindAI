from enum import Enum


class RuntimeState(str, Enum):

    CREATED = "created"

    RUNNING = "running"

    STOPPED = "stopped"