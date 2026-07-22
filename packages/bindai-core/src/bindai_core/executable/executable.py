from __future__ import annotations

from abc import ABC, abstractmethod

from bindai_core.context import ExecutionContext

from .result import ExecutionResult


class Executable(ABC):
    """
    Base contract for every executable component in BindAI.
    """

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """
        Execute this component.
        """
        raise NotImplementedError
