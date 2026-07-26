from __future__ import annotations

from bindai_core.tool import ToolRegistry
from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable

from bindai_prompts import Prompt

from bindai_memory import (
    Memory,
    InMemoryProvider,
)

from .conversation import Conversation
from .execution.engine import AgentExecutionEngine
from .execution.data import ExecutionData
from .configuration import AgentConfiguration
from .result import AgentResult
from bindai_core.events import EventBus
from bindai_core.events import ToolExecutedEvent
from bindai_core.context import ExecutionContext

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
        prompt: Prompt | None = None,
    ):

        self.name = name
        self.provider = provider

        self.prompt = prompt or Prompt()

        if instructions:
            self.prompt.system = instructions

        self.events = EventBus()

        self.retriever = None
        self.knowledge = None

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

        self.hooks = []

    @property
    def instructions(self) -> str:

        return self.prompt.system

    @instructions.setter
    def instructions(
        self,
        value: str,
    ):

        self.prompt.system = value

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

        return self.execute(
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

        self.tools.register(
            tool,
        )

        return self

    def execute(
        self,
        context: ExecutionContext,
    ) -> AgentResult:

        return self.executor.execute(
            self,
            context,
        )

    def execute_tool(
        self,
        name: str,
        **kwargs,
    ):

        result = self.tools.execute(
            name,
            **kwargs,
        )

        self.events.publish(
            ToolExecutedEvent(
                tool_name=name,
            )
        )

        return result

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

    def use_retriever(
        self,
        retriever,
    ) -> "Agent":

        self.retriever = retriever

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