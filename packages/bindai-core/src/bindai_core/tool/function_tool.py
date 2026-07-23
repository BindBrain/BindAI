from __future__ import annotations

from typing import Any, Callable

from .definition import ToolDefinition

from .result import ToolResult
from .base import Tool

from .inspector import ToolInspector

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext


class FunctionTool(Tool):
    """
    Wraps a Python function as a BindAI Tool.
    """

    def __init__(
        self,
        function: Callable[..., Any],
        name: str | None = None,
    ):

        self.function = function

        self._name = name or function.__name__

    @property
    def name(self) -> str:

        return self._name

    @property
    def description(self) -> str:

        return (self.function.__doc__ or "").strip()

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    @property
    def parameters(
        self,
    ) -> dict[str, Any]:

        return ToolInspector.parameters(
            self.function,
        )

    def execute(
        self,
        context: ExecutionContext | None = None,
        **kwargs,
    ) -> ToolResult:

        try:
            result = self.function(
                **kwargs,
            )

            return ToolResult(
                success=True,
                output=result,
            )

        except Exception as ex:
            return ToolResult(
                success=False,
                error=str(ex),
            )
