from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from bindai_core.context import ExecutionContext

TResult = TypeVar("TResult")


class Executable(ABC, Generic[TResult]):
    """
    Base contract for every executable component in BindAI.
    """

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> TResult:
        ...