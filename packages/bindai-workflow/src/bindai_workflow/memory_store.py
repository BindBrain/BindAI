from __future__ import annotations

from .instance import WorkflowInstance
from .store import WorkflowStore


class MemoryWorkflowStore(
    WorkflowStore,
):

    def __init__(self):

        self.instances = {}

    def save(
        self,
        instance: WorkflowInstance,
    ):

        self.instances[
            instance.id
        ] = instance

    def load(
        self,
        instance_id: str,
    ):

        return self.instances.get(
            instance_id,
        )

    def delete(
        self,
        instance_id: str,
    ):

        self.instances.pop(
            instance_id,
            None,
        )