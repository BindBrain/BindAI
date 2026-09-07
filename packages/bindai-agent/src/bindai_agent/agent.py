from __future__ import annotations

from collections.abc import Callable
from typing import Any

from bindai_core.context import ExecutionContext
from bindai_core.events import EventBus, ToolExecutedEvent
from bindai_core.executable import Executable
from bindai_core.tool import ToolRegistry
from bindai_memory import InMemoryProvider, Memory
from bindai_prompts import Prompt

from .delegation import AgentDelegationTool
from .configuration import AgentConfiguration
from .conversation import Conversation
from .execution.data import ExecutionData
from .execution.engine import AgentExecutionEngine
from .provider_resolver import resolve_provider
from .result import AgentResult
from .state import AgentState


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

        self.name: str = name

        if isinstance(provider, str):
            self.provider = resolve_provider(provider)
        else:
            self.provider = provider

        self.prompt: Prompt = prompt or Prompt()

        if instructions:
            self.prompt.system = instructions

        self.events: EventBus = EventBus()

        self.retriever: Any | None = None
        self.knowledge: Any | None = None

        self.conversation: Conversation = Conversation()

        self.memory: Memory = Memory(
            InMemoryProvider(),
        )

        self.tools: ToolRegistry = ToolRegistry()

        self.configuration: AgentConfiguration = AgentConfiguration()

        self.state: AgentState = AgentState.IDLE

        self.executor: AgentExecutionEngine = AgentExecutionEngine(self)

        self.middleware: list[Any] = []

        self.hooks: list[Any] = []

        self.callbacks: dict[str, list[Callable[..., Any]]] = {
            "before_run": [],
            "after_run": [],
            "error": [],
        }

    @property
    def instructions(self) -> str:
        return self.prompt.system or ""

    @instructions.setter
    def instructions(
        self,
        value: str,
    ):

        self.prompt.system = value

    def _create_context(
        self,
        message: str,
        output: type | None = None,
    ) -> ExecutionContext:

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

        return context

    def run(
        self,
        message: str,
        output: type | None = None,
    ) -> AgentResult:
        """
        Primary execution entry point.
        """

        return self.chat(
            message,
            output,
        )

    @staticmethod
    def builder():
        from .builder import AgentBuilder
        return AgentBuilder()

    def chat(
        self,
        message: str,
        output: type | None = None,
    ) -> AgentResult:

        return self.execute(
            self._create_context(
                message,
                output,
            ),
        )

    def stream_chat(
        self,
        message: str,
        output: type | None = None,
    ):

        return self.executor.stream(
            self,
            self._create_context(
                message,
                output,
            ),
        )

    def stream(
        self,
        context: ExecutionContext,
    ):

        return self.executor.stream(
            self,
            context,
        )

    def tool(
        self,
        tool: Any,
    ) -> Agent:

        self.tools.register(
            tool,
        )

        return self

    def add_tool(
        self,
        tool: Any,
    ) -> Agent:
        """
        Backwards-compatible alias for tool().
        """

        return self.tool(
            tool,
        )

    def delegate_to(
        self,
        agent: Agent,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> Agent:
        self.tool(
            AgentDelegationTool(
                agent,
                name=name,
                description=description,
            )
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
        **kwargs: Any,
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
        middleware: Any,
    ) -> Agent:

        self.middleware.append(
            middleware,
        )

        return self

    def use_memory(
        self,
        memory: Memory,
    ) -> Agent:

        self.memory = memory

        return self

    def use_retriever(
        self,
        retriever: Any,
    ) -> Agent:

        self.retriever = retriever

        return self

    def use_knowledge(
        self,
        knowledge: Any,
    ) -> Agent:

        self.knowledge = knowledge

        return self

    def hook(
        self,
        hook: Callable[..., Any],
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
        callback: Callable[..., Any],
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
        *args: Any,
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
