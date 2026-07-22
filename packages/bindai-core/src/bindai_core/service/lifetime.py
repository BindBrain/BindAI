from enum import Enum


class ServiceLifetime(str, Enum):
    SINGLETON = "singleton"

    TRANSIENT = "transient"
