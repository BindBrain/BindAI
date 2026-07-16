from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.model import (
    ModelRequest,
)
from bindai_core.tool import Tool, ToolRegistry

from .agent import Agent
from .result import AgentResult


class AssistantAgent(Agent):
    """
    Standard conversational AI agent.
    """

    def __init__(
        self,
        name: str,
        instructions: str,
        provider,
    ):
        super().__init__(
            name=name,
            instructions=instructions,
            provider=provider,
        )

        self.tools = ToolRegistry()

    def register_tool(
        self,
        tool: Tool,
    ):
        self.tools.register(tool)

    def execute_tool(
        self,
        tool_name: str,
        **kwargs,
    ):
        return self.tools.execute(
            tool_name,
            **kwargs,
        )

    def execute(
        self,
        context: ExecutionContext,
    ) -> AgentResult:

        user_input = context.variables.get(
            "input",
            "",
        )

        if len(self.conversation) == 0:
            self.conversation.add_system(
                self.instructions,
            )

        self.conversation.add_user(
            user_input,
        )

        request = self.conversation.to_request()

        response = self.provider.generate(
            request,
        )

        # Automatic tool execution
        if response.tool_call is not None:

            tool_result = self.execute_tool(
                response.tool_call.name,
                **response.tool_call.arguments,
            )

            tool_output = str(tool_result.output)

            self.conversation.add_assistant(
                tool_output,
            )

            return AgentResult(
                success=tool_result.success,
                output=tool_output,
            )

        # Normal assistant response
        self.conversation.add_assistant(
            response.content,
        )

        return AgentResult(
            success=True,
            output=response.content,
        )