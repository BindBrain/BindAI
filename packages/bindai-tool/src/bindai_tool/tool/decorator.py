import inspect

from .metadata import ToolMetadata


def tool(
    name=None,
    description=None,
):
    def wrapper(func):

        func.__bind_tool__ = True

        func.__metadata__ = ToolMetadata(

            name=name or func.__name__,

            description=description or "",

        )

        func.__signature__ = inspect.signature(func)

        return func

    return wrapper