from dataclasses import dataclass


@dataclass(slots=True)
class WorkflowNode:

    id: str

    executable: object