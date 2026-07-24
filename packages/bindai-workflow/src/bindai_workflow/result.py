from dataclasses import dataclass

from bindai_core.executable import ExecutionResult


@dataclass(slots=True)
class WorkflowResult(ExecutionResult):
    success: bool

    output: object = None

    error: str | None = None