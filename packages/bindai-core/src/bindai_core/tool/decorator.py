from __future__ import annotations

from typing import Callable

from .function_tool import FunctionTool


def tool(
    function: Callable | None = None,
    *,
    name: str | None = None,
):
    """
    Decorator that converts a Python function
    into a BindAI Tool.

    Supports:

        @tool

        @tool()

        @tool(name="calculator")
    """

    def decorator(
        func: Callable,
    ):

        return FunctionTool(
            function=func,
            name=name,
        )

    #
    # @tool
    #

    if function is not None:
        return decorator(
            function,
        )

    #
    # @tool(...)
    #

    return decorator
