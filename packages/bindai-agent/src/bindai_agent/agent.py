from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.tool import ToolRegistry

from .conversation import Conversation
from .execution.engine import AgentExecutionEngine

from bindai_memory import (
    Memory,
    InMemoryProvider,
)

from .configuration import AgentConfiguration
from .execution.data import ExecutionData

from bindai_core.executable import Executable


class Agent(Executable):
    """
    Base AI agent.
    """

    def __init__(
        self,
        *,
        name: str,
        provider,
        instructions: str = "",
    ):

        self.name = name
        self.provider = provider
        self.instructions = instructions

        self.conversation = Conversation()
        self.memory = Memory(
            InMemoryProvider(),
        )
        self.tools = ToolRegistry()
        self.configuration = AgentConfiguration()

        self.executor = AgentExecutionEngine(
            self,
        )

        self.middleware = []

        self.knowledge = None

        self.hooks = []

    def chat(
        self,
        message: str,
        output: type | None = None,
    ):

        context = ExecutionContext()

        context.data = ExecutionData()

        context.variables.set(
            "input",
            message,
        )

        context.variables.set(
            "output_type",
            output,
        )

        return self.executor.execute(
            self,
            context,
        )

    def stream(
        self,
        message: str,
        output: type | None = None,
    ):

        context = ExecutionContext()

        context.data = ExecutionData()

        context.variables.set(
            "input",
            message,
        )

        context.variables.set(
            "output_type",
            output,
        )

        return self.executor.stream(
            self,
            context,
        )

    def tool(
        self,
        tool,
    ) -> "Agent":
        """
        Register a tool.
        """

        self.tools.register(
            tool,
        )

        return self

    def execute(
        self,
        context,
    ):

        return self.executor.execute(
            self,
            context,
        )

    def execute_tool(
        self,
        name: str,
        **kwargs,
    ):
        """
        Execute a registered tool.
        """

        return self.tools.execute(
            name,
            **kwargs,
        )

    def use_middleware(
        self,
        middleware,
    ) -> "Agent":

        self.middleware.append(
            middleware,
        )

        return self

    def use_memory(
        self,
        memory,
    ) -> "Agent":

        self.memory = memory

        return self

    def use_knowledge(
        self,
        knowledge,
    ) -> "Agent":

        self.knowledge = knowledge

        return self

    def hook(
        self,
        hook,
    ) -> "Agent":

        self.hooks.append(
            hook,
        )

        return self

    def session(self):

        from .session import AgentSession

        return AgentSession(
            self,
        )
