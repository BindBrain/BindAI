from __future__ import annotations

from collections.abc import Callable
from typing import Any, overload

from .function_tool import FunctionTool


@overload
def tool(func: Callable[..., Any]) -> FunctionTool: ...


@overload
def tool(
    *,
    name: str | None = None,
) -> Callable[[Callable[..., Any]], FunctionTool]: ...


def tool(
    func: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
) -> FunctionTool | Callable[[Callable[..., Any]], FunctionTool]:
    """
    Supports:

        @tool

        @tool()

        @tool(name="calculator")
    """

    def decorator(
        func: Callable[..., Any],
    ) -> FunctionTool:
        return FunctionTool(
            function=func,
            name=name,
        )

    if func is not None:
        return decorator(func)

    return decorator
