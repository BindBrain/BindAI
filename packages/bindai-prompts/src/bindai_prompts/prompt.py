from dataclasses import dataclass


@dataclass(slots=True)
class Prompt:
    system: str = ""

    user: str = ""

    assistant: str = ""
