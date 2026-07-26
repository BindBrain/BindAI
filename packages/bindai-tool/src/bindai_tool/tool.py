from __future__ import annotations

from abc import abstractmethod

from bindai_core.context import ExecutionContext
from bindai_core.runnable import Runnable

from .result import ToolResult


class Tool(Runnable):
    """
    Base class for every BindAI tool.
    """

    name: str = ""

    description: str = ""

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> ToolResult:
        ...