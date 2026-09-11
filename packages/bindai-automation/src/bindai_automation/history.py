from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .run import AutomationRun


class AutomationRunHistory(ABC):
    """
    History contract for completed and attempted automation runs.
    """

    @abstractmethod
    def record(self, run: AutomationRun) -> None:
        ...

    @abstractmethod
    def get(self, run_id: str) -> AutomationRun | None:
        ...

    @abstractmethod
    def list(self) -> tuple[AutomationRun, ...]:
        ...