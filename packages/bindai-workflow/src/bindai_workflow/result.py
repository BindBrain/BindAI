from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowResult:

    success: bool

    output: object = None

    error: str | None = None