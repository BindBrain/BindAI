from __future__ import annotations

from collections.abc import Callable

from .tool_result import ToolResult


class Tool:
    """
    Represents a callable tool.
    """

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
    ):
        self.name = name
        self.description = description
        self.function = function

    def __call__(self, *args, **kwargs) -> ToolResult:

        try:
            value = self.function(*args, **kwargs)

            return ToolResult(
                success=True,
                value=value,
            )

        except Exception as e:

            return ToolResult(
                success=False,
                error=str(e),
            )