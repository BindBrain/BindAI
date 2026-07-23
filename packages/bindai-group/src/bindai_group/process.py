from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .result import GroupResult


class Process(ABC):
    """
    Base execution strategy.
    """

    @abstractmethod
    def execute(
        self,
        group,
    ) -> GroupResult:
        ...