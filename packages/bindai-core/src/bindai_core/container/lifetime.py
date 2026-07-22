from enum import Enum


class ServiceLifetime(str, Enum):
    """
    Defines how long a service instance lives.
    """

    SINGLETON = "singleton"
    TRANSIENT = "transient"
