from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionSnapshot:
    execution_id: str

    state: object

    variables: dict

    metadata: dict

    timestamp: str
