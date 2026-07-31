from enum import StrEnum


class ServiceLifetime(StrEnum):
    """
    Defines how long a service instance lives.
    """

    SINGLETON = "singleton"
    TRANSIENT = "transient"
