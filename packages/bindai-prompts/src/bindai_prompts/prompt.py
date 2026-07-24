from dataclasses import dataclass


@dataclass(slots=True)
class Prompt:

    system: str | None = None

    user: str = ""

    assistant: str | None = None