from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bindai_core.context import ExecutionContext
from bindai_tool import Tool, ToolResult

from .executable_node import ExecutableNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class ToolNode(ExecutableNode):
    """
    Executes a BindAI Tool.

    During Studio simulation, the real tool is not executed. Instead a
    simulated ToolResult is produced so the workflow can continue without
    triggering the tool's real side effects.
    """

    def __init__(
        self,
        node_id: str,
        tool: Tool,
        output_variable: str = "tool_output",
        parameter_mapping: dict[str, str] | None = None,
        name: str | None = None,
    ):
        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.tool = tool
        self.parameter_mapping = parameter_mapping or {}
        self.output_variable = output_variable

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        if context.metadata.get("bindai_simulation") is True:
            result = ToolResult.ok(
                {
                    "simulated": True,
                    "tool": self.tool.name,
                }
            )
            return self.after_execute(context, result)

        execution_context = ExecutionContext()
        execution_context.variables = context.variables.copy()

        execution_context.metadata.update(getattr(context, "metadata", {}))

        if self.parameter_mapping:
            for parameter, variable in self.parameter_mapping.items():
                value = context.get(variable)

                if hasattr(value, "value") and hasattr(value, "success"):
                    value = value.value

                execution_context.variables.set(parameter, value)

        result = self.tool.execute(execution_context)
        return self.after_execute(context, result)

    def get_executable(
        self,
        context: WorkflowContext,
    ) -> Tool:
        return self.tool

    def after_execute(
        self,
        context: WorkflowContext,
        result: ToolResult,
    ) -> WorkflowContext:
        context.set(self.output_variable, result)
        return context

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "tool": self.tool.name,
                "output_variable": self.output_variable,
                "parameter_mapping": self.parameter_mapping,
            }
        )
        return data

    def load_dict(
        self,
        data: dict[str, Any],
    ) -> None:
        super().load_dict(data)
        self.tool = data["tool"]
        self.output_variable = data.get(
            "output_variable",
            "tool_output",
        )
        self.parameter_mapping = data.get(
            "parameter_mapping",
            {},
        )
