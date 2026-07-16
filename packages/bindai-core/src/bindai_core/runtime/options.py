from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeOptions:
    """
    Runtime configuration.
    """

    debug: bool = False