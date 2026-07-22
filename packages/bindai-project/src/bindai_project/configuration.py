from dataclasses import dataclass


@dataclass(slots=True)
class ProjectConfiguration:
    name: str

    version: str = "1.0.0"

    description: str = ""
