from dataclasses import dataclass


@dataclass(slots=True)
class HostConfiguration:

    name: str = "BindAI"

    version: str = "1.0.0"