from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext
from bindai_tool import Tool, ToolDefinition, ToolResult

if TYPE_CHECKING:
    from .team import AgentTeam


class AgentTeamDelegationTool(Tool):
    """
    Exposes an AgentTeam as a tool so an agent can delegate
    a task to the team.
    """

    def __init__(
        self,
        team: AgentTeam,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        self.team = team
        self._name = name or f"delegate_to_{team.name.lower().replace(' ', '_')}"
        self._description = description or f"Delegate a task to the {team.name} agent team."

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
                        "description": "Task or message to send to the agent team.",
                    }
                },
                "required": ["message"],
            },
        )

    def execute(self, context: ExecutionContext) -> ToolResult:
        message = context.variables.get("message")

        if not message:
            return ToolResult.failed("Team delegation requires a non-empty message.")

        result = self.team.run(str(message))

        if result.success:
            return ToolResult.ok(result.output)

        return ToolResult.failed(
            result.error or "Agent team execution failed.",
        )
