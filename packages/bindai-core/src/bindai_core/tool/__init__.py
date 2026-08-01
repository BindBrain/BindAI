"""
Compatibility exports.

Implementation lives in bindai_tool.
"""

from bindai_tool import (
    FunctionTool,
    Tool,
    ToolDefinition,
    ToolRegistry,
    ToolResult,
    tool,
)

__all__ = [
    "Tool",
    "ToolDefinition",
    "FunctionTool",
    "ToolRegistry",
    "ToolResult",
    "tool",
]
