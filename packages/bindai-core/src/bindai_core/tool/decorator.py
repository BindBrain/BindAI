from __future__ import annotations

from typing import Callable

from .function_tool import FunctionTool


def tool(
    name: str | None = None,
):
    """
    Decorator that converts a Python function
    into a BindAI Tool.
    """

    def wrapper(
        function: Callable,
    ):

        return FunctionTool(
            function=function,
            name=name,
        )

    return wrapper