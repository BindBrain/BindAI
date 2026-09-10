from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .run import AutomationRun


class AutomationStateStore(ABC):
    """
    Persistence contract for automation runs.
    """

    @abstractmethod
    def save(self, run: AutomationRun) -> None:
        ...

    @abstractmethod
    def load(self, run_id: str) -> AutomationRun | None:
        ...

    @abstractmethod
    def delete(self, run_id: str) -> None:
        ...