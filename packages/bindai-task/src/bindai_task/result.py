from dataclasses import dataclass

from bindai_core.executable.result import ExecutionResult


@dataclass(slots=True)
class TaskResult(ExecutionResult):
    output: str | None = None