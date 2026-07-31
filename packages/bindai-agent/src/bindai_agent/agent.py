from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.events import EventBus, ToolExecutedEvent
from bindai_core.executable import Executable
from bindai_core.tool import ToolRegistry
from bindai_memory import (
    InMemoryProvider,
    Memory,
)
from bindai_prompts import Prompt

from .configuration import AgentConfiguration
from .conversation import Conversation
from .execution.data import ExecutionData
from .execution.engine import AgentExecutionEngine
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

        self.callbacks = {
            "before_run": [],
            "after_run": [],
            "error": [],
        }

    @property
    def instructions(self) -> str:

        return self.prompt.system

    @instructions.setter
    def instructions(
        self,
        value: str,
    ):

        self.prompt.system = value

    def run(
        self,
        message: str,
        output: type | None = None,
    ):
        """
        Primary execution entry point.
        """

        return self.chat(
            message,
            output,
        )

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
    ) -> Agent:

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
    ) -> Agent:

        self.middleware.append(
            middleware,
        )

        return self

    def use_memory(
        self,
        memory,
    ) -> Agent:

        self.memory = memory

        return self

    def use_retriever(
        self,
        retriever,
    ) -> Agent:

        self.retriever = retriever

        return self

    def use_knowledge(
        self,
        knowledge,
    ) -> Agent:

        self.knowledge = knowledge

        return self

    def hook(
        self,
        hook,
    ) -> Agent:

        self.hooks.append(
            hook,
        )

        return self

    def before_run(
        self,
        context: ExecutionContext,
    ) -> None:

        self.emit(
            "before_run",
            self,
            context,
        )

    def after_run(
        self,
        context: ExecutionContext,
        result: AgentResult,
    ) -> None:

        self.emit(
            "after_run",
            self,
            context,
            result,
        )

    def on_error(
        self,
        context: ExecutionContext,
        error: Exception,
    ) -> None:

        self.emit(
            "error",
            self,
            context,
            error,
        )

    def on(
        self,
        event: str,
        callback,
    ) -> Agent:

        self.callbacks.setdefault(
            event,
            [],
        ).append(
            callback,
        )

        return self

    def emit(
        self,
        event: str,
        *args,
    ) -> None:

        for callback in self.callbacks.get(
            event,
            [],
        ):
            callback(
                *args,
            )

    def session(self):

        from .session import AgentSession

        return AgentSession(
            self,
        )
