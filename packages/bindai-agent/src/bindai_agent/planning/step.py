from dataclasses import dataclass


@dataclass
class PlanStep:
    description: str

    tool: str | None = None

    completed: bool = False
