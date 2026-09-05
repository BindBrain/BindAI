from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext
from bindai_tool import Tool, ToolDefinition, ToolResult

if TYPE_CHECKING:
    from .agent import Agent


class AgentDelegationTool(Tool):
    """
    Exposes another Agent as a tool so an agent can delegate tasks to it.
    """

    def __init__(
        self,
        agent: Agent,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        self.agent = agent
        self._name = name or f"delegate_to_{agent.name}"
        self._description = (
            description
            or f"Delegate a task to the {agent.name} agent."
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Task or message to send to the delegated agent.",
                    }
                },
                "required": ["message"],
            },
        )

    def execute(
        self,
        context: ExecutionContext,
    ) -> ToolResult:
        message = context.variables.get("message")

        if not message:
            return ToolResult.failed(
                "Delegation requires a non-empty message."
            )

        result = self.agent.run(
            str(message),
        )

        if result.success:
            return ToolResult.ok(
                result.output,
            )

        return ToolResult.failed(
            result.error or "Delegated agent execution failed.",
        )