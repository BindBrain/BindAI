from __future__ import annotations

from .instance import WorkflowInstance
from .store import WorkflowStore


class MemoryWorkflowStore(
    WorkflowStore,
):
    def __init__(self):

        self.instances: dict[str, WorkflowInstance] = {}

    def save(
        self,
        instance: WorkflowInstance,
    ) -> None:

        self.instances[instance.id] = instance

    def load(
        self,
        instance_id: str,
    ) -> WorkflowInstance | None:

        return self.instances.get(
            instance_id,
        )

    def delete(
        self,
        instance_id: str,
    ) -> None:

        self.instances.pop(
            instance_id,
            None,
        )
