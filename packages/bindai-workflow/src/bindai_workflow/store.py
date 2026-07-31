from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import WorkflowInstance


class WorkflowStore(ABC):
    """
    Persists workflow instances.
    """

    @abstractmethod
    def save(
        self,
        instance: WorkflowInstance,
    ) -> None: ...

    @abstractmethod
    def load(
        self,
        instance_id: str,
    ) -> WorkflowInstance | None: ...

    @abstractmethod
    def delete(
        self,
        instance_id: str,
    ) -> None: ...
