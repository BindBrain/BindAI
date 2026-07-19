from dataclasses import dataclass

from bindai_core.executable import ExecutionResult


@dataclass(slots=True)
class RuntimeResult:

    execution: ExecutionResult

    duration_ms: float