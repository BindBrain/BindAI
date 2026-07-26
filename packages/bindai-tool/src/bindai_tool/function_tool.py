from __future__ import annotations

from typing import Any
from typing import Callable
from typing import TYPE_CHECKING

from bindai_core.tool.definition import ToolDefinition
from bindai_core.tool.inspector import ToolInspector

from .result import ToolResult
from .tool import Tool

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
    def parameters(
        self,
    ) -> dict[str, Any]:

        return ToolInspector.parameters(
            self.function,
        )

    @property
    def definition(
        self,
    ) -> ToolDefinition:

        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    def execute(
        self,
        context: ExecutionContext,
        **kwargs,
    ) -> ToolResult:

        try:

            #
            # Backwards compatibility.
            #
            # Older callers still invoke:
            #
            # tool.execute(context, a=1, b=2)
            #
            # Copy them into the execution context.
            #

            if kwargs:

                for key, value in kwargs.items():

                    context.variables.set(
                        key,
                        value,
                    )

            result = self.function(
                **context.variables.as_dict(),
            )

            return ToolResult(
                success=True,
                output=result,
            )

        except Exception as ex:

            return ToolResult(
                success=False,
                output=None,
                error=str(ex),
            )