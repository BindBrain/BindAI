from __future__ import annotations

from builtins import list as builtin_list

from .tool import Tool


class ToolRegistry:
    """
    Stores available tools.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:

        self._tools[tool.name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:

        self._tools.pop(name, None)

    def get(
        self,
        name: str,
    ) -> Tool | None:

        return self._tools.get(name)

    #
    # Primary API
    #

    def all_tools(self) -> list[Tool]:
        return list(self._tools.values())

    #
    # Backward compatibility
    #

    def list(self):
        return self.all_tools()

    def all(self) -> builtin_list[Tool]:
        return self.all_tools()

    def names(self) -> builtin_list[str]:
        return list(self._tools.keys())

    def __contains__(self, name: str):
        return name in self._tools

    def __len__(self):
        return len(self._tools)
