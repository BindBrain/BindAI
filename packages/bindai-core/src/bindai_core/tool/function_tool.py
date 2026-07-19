from __future__ import annotations

import inspect
from typing import Any, Callable

from .result import ToolResult
from .tool import Tool


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

        self._name = (
            name
            or function.__name__
        )

    @property
    def name(self) -> str:

        return self._name

    @property
    def description(self) -> str:

        return (
            self.function.__doc__
            or ""
        ).strip()

    @property
    def parameters(self) -> dict[str, Any]:
        """
        Build a provider-agnostic parameter schema
        from the wrapped Python function signature.
        """

        signature = inspect.signature(
            self.function,
        )

        schema: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():

            annotation = parameter.annotation

            if annotation is int:
                parameter_type = "integer"

            elif annotation is float:
                parameter_type = "number"

            elif annotation is bool:
                parameter_type = "boolean"

            elif annotation is list:
                parameter_type = "array"

            elif annotation is dict:
                parameter_type = "object"

            else:
                parameter_type = "string"

            schema[name] = {
                "type": parameter_type,
                "required": (
                    parameter.default
                    is inspect.Parameter.empty
                ),
            }

        return schema

    def execute(
        self,
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