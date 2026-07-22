from dataclasses import dataclass


@dataclass(slots=True)
class ApplicationConfiguration:
    name: str = "BindAI"

    debug: bool = False
