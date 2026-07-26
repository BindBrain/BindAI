from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.context import ExecutionContext
from bindai_core.executable.result import ExecutionResult


class Runnable(ABC):
    """
    Common execution interface for every BindAI component.
    """

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult:
        ...

    def stream(
        self,
        context: ExecutionContext,
    ):
        """
        Optional streaming interface.
        """

        raise NotImplementedError(
            f"{type(self).__name__} does not support streaming."
        )