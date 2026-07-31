from __future__ import annotations

from abc import ABC, abstractmethod

from bindai_core.context import ExecutionContext

from .result import GroupResult


class Process(ABC):
    """
    Base execution strategy.
    """

    @abstractmethod
    def execute(
        self,
        group,
        context: ExecutionContext,
    ) -> GroupResult: ...
