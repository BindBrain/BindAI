from __future__ import annotations

from collections.abc import Callable

from .tool import Tool


def tool(
    function: Callable | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
):
    """
    Decorator that converts a function into a Tool.
    """

    def decorator(func: Callable):

        return Tool(
            name=name or func.__name__,
            description=description or (func.__doc__ or ""),
            function=func,
        )

    if function is None:
        return decorator

    return decorator(function)
