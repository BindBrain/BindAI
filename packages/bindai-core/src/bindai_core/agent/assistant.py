from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.tool import (
    Tool,
    ToolRegistry,
)

from .agent import Agent
from .executor import AgentExecutor
from .result import AgentResult


class AssistantAgent(Agent):
    """
    Standard conversational AI agent.

    The AssistantAgent is responsible for:

    - holding agent configuration
    - registering tools
    - delegating execution to AgentExecutor
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
    ) -> None:
        """
        Register a tool available to this agent.
        """

        self.tools.register(tool)

    def execute_tool(
        self,
        tool_name: str,
        **kwargs,
    ):
        """
        Execute a registered tool.
        """

        return self.tools.execute(
            tool_name,
            **kwargs,
        )

    def execute(
        self,
        context: ExecutionContext,
    ) -> AgentResult:
        """
        Execute the agent using the AgentExecutor.
        """

        executor = AgentExecutor()

        return executor.execute(
            self,
            context,
        )
