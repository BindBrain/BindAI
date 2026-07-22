from dataclasses import dataclass, field

from .step import PlanStep


@dataclass
class ExecutionPlan:

    steps: list[PlanStep] = field(
        default_factory=list,
    )

    current_step: int = 0

    completed: bool = False