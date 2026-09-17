from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_tool import Tool

from .executable_node import ExecutableNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class ToolNode(
    ExecutableNode,
):
    """
    Executes a BindAI Tool.
    """

    def __init__(
        self,
        node_id: str,
        tool: Tool,
        output_variable: str = "tool_output",
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.tool = tool
        self.output_variable = output_variable

    def get_executable(
        self,
        context: WorkflowContext,
    ) -> Tool:

        return self.tool

    def after_execute(
        self,
        context: WorkflowContext,
        result,
    ) -> WorkflowContext:

        context.set(
            self.output_variable,
            result,
        )

        return context

    def to_dict(
        self,
    ) -> dict:

        data = super().to_dict()

        data.update(
            {
                "tool": self.tool.name,
                "output_variable": self.output_variable,
            }
        )

        return data

    def load_dict(
        self,
        data: dict,
    ) -> None:

        super().load_dict(
            data,
        )

        self.tool = data["tool"]

        self.output_variable = data.get(
            "output_variable",
            "tool_output",
        )
