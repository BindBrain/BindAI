from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.context import ExecutionContext

from .result import ToolResult


class Tool(ABC):
    """
    Base class for every BindAI tool.
    """

    name: str = ""

    description: str = ""

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
        **kwargs,
    ) -> ToolResult:
        ...