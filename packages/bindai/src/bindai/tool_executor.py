from __future__ import annotations

from .tool_registry import ToolRegistry
from .tool_result import ToolResult


class ToolExecutor:
    """
    Executes tools from a registry.
    """

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        *args,
        **kwargs,
    ) -> ToolResult:

        tool = self.registry.get(tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                error=f"Unknown tool '{tool_name}'",
            )

        return tool(*args, **kwargs)
