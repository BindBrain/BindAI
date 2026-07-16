from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowEdge:

    source: str

    target: str