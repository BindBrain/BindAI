from __future__ import annotations

from .tool import Tool


class ToolRegistry:
    """
    Registry of tools available to an agent.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> Tool:
        return self._tools[tool_name]

    def execute(self, tool_name: str, **kwargs):
        tool = self.get(tool_name)
        return tool.execute(**kwargs)

    def names(self):
        return list(self._tools.keys())

    def __len__(self):
        return len(self._tools)