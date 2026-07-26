from __future__ import annotations

from bindai_core.context import ExecutionContext

from .exceptions import ToolAlreadyRegistered
from .exceptions import ToolNotFound

from .tool import Tool
from bindai_tool.function_tool import FunctionTool

class ToolRegistry:
    def __init__(self):

        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ):

        if callable(tool):
            tool = FunctionTool(tool)

        if tool.name in self._tools:
            raise ToolAlreadyRegistered(
                tool.name,
            )

        self._tools[tool.name] = tool

    def get(
        self,
        name: str,
    ) -> Tool:

        if name not in self._tools:
            raise ToolNotFound(
                name,
            )

        return self._tools[name]

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def remove(
        self,
        name: str,
    ):

        self._tools.pop(
            name,
            None,
        )

    def clear(
        self,
    ):

        self._tools.clear()

    def all(
        self,
    ) -> list[Tool]:

        return list(
            self._tools.values(),
        )

    def definitions(
        self,
    ):

        return [tool.definition for tool in self._tools.values()]

    def execute(
        self,
        name: str,
        **kwargs,
    ):

        context = ExecutionContext()

        for key, value in kwargs.items():
            context.variables.set(
                key,
                value,
            )

        return self.get(
            name,
        ).execute(
            context,
        )

    def __len__(
        self,
    ):

        return len(
            self._tools,
        )
