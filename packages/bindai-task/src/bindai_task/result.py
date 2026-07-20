from dataclasses import dataclass


@dataclass(slots=True)
class TaskResult:

    success: bool

    output: str | None = None

    error: str | None = None