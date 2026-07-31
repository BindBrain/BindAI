from __future__ import annotations

from bindai_core.tool import Tool, ToolDefinition


class ToolRegistry:
    """
    Stores every tool available to an agent.
    """

    def __init__(self):

        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool,
    ) -> None:

        self._tools[tool.definition.name] = tool

    def get(
        self,
        name: str,
    ):

        return self._tools[name]

    def definitions(
        self,
    ) -> list[ToolDefinition]:

        return [tool.definition for tool in self._tools.values()]

    def all(
        self,
    ):

        return list(self._tools.values())

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def __len__(
        self,
    ) -> int:

        return len(self._tools)
