from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowConfiguration:
    name: str
