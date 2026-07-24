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

        self.middleware: list[object] = []

        self.retriever = None

        self.hooks: list[object] = []

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

        self.tools.register(
            tool,
        )

        return self

    def execute(
        self,
        context: ExecutionContext,
    ) -> AgentResult:

        result = self.executor.execute(
            self,
            context,
        )

        if isinstance(
            result,
            AgentResult,
        ):
            return result

        return AgentResult(
            success=True,
            output=result,
        )

    def execute_tool(
        self,
        name: str,
        **kwargs,
    ):

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