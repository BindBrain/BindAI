from __future__ import annotations

from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from bindai_core.context import ExecutionContext
from bindai_core.runnable import Runnable

TResult = TypeVar("TResult")


class Executable(
    Runnable,
    Generic[TResult],
):
    """
    Base contract for every executable component.
    """

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> TResult:
        ...