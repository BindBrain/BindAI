from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from .result import ToolResult

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext


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