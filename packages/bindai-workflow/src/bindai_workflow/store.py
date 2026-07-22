from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .instance import WorkflowInstance


class WorkflowStore(ABC):
    """
    Persists workflow instances.
    """

    @abstractmethod
    def save(
        self,
        instance: WorkflowInstance,
    ): ...

    @abstractmethod
    def load(
        self,
        instance_id: str,
    ) -> WorkflowInstance | None: ...

    @abstractmethod
    def delete(
        self,
        instance_id: str,
    ): ...
