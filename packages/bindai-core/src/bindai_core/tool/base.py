from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from .result import ToolResult

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext
    from .definition import ToolDefinition


class Tool(ABC):
    """
    Base class for every BindAI tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        ...

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
        **kwargs,
    ) -> ToolResult:
        ...