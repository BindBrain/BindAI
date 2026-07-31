from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .definition import ToolDefinition
from .inspector import ToolInspector
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
        description: str | None = None,
    ):
        self.function = function

        self._name = name or function.__name__

        self._description = description or (function.__doc__ or "").strip()

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return ToolInspector.parameters(
            self.function,
        )

    def execute(
        self,
        context: ExecutionContext,
        **overrides,
    ) -> ToolResult:
        try:
            kwargs = context.variables.as_dict()

            kwargs.update(
                overrides,
            )

            result = self.function(
                **kwargs,
            )

            return ToolResult(
                success=True,
                value=result,
            )

        except Exception as ex:
            return ToolResult(
                success=False,
                value=None,
                error=str(ex),
            )

    def __call__(
        self,
        *args,
        **kwargs,
    ):
        """
        Backwards-compatible callable interface.
        """

        from bindai_core.context import ExecutionContext

        context = ExecutionContext()

        #
        # Positional arguments
        #

        parameter_names = list(self.parameters.keys())

        for name, value in zip(
            parameter_names,
            args,
        ):
            context.variables.set(
                name,
                value,
            )

        #
        # Keyword arguments
        #

        for key, value in kwargs.items():
            context.variables.set(
                key,
                value,
            )

        return self.execute(
            context,
        )
