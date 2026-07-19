from __future__ import annotations

from abc import ABC

from bindai_core.context import ExecutionContext
from bindai_core.conversation import Conversation
from bindai_core.executable import Executable
from bindai_core.model import ModelProvider
from bindai_core.tool import Tool, ToolRegistry

from .configuration import AgentConfiguration
from .result import AgentResult
from .state import AgentState


class Agent(Executable, ABC):
    """
    Base class for every BindAI agent.

    The Agent is responsible only for holding state and
    configuration.

    All execution is delegated to AgentExecutor.
    """

    def __init__(
        self,
        *,
        name: str,
        instructions: str,
        provider: ModelProvider,
        configuration: AgentConfiguration | None = None,
    ):

        self.configuration = (
            configuration
            or AgentConfiguration()
        )

        self.configuration.name = name
        self.configuration.instructions = instructions

        self.provider = provider

        #
        # Conversation
        #

        self.conversation = Conversation()

        #
        # Tools
        #

        self.tools = ToolRegistry()

        #
        # Runtime state
        #

        self.state = AgentState.IDLE

        #
        # Optional runtime services
        #

        self.memory = None

        self.knowledge = None

        self.middleware = []

    #
    # Properties
    #

    @property
    def name(
        self,
    ) -> str:

        return self.configuration.name

    @property
    def instructions(
        self,
    ) -> str:

        return self.configuration.instructions

    #
    # Tool registration
    #

    def register_tool(
        self,
        tool: Tool,
    ) -> None:

        self.tools.register(
            tool,
        )

    #
    # Runtime extensions
    #

    def use_memory(
        self,
        memory,
    ):

        self.memory = memory

        return self

    def use_knowledge(
        self,
        knowledge,
    ):

        self.knowledge = knowledge

        return self

    def use_middleware(
        self,
        middleware,
    ):

        self.middleware.append(
            middleware,
        )

        return self

    #
    # High level helpers
    #

    def chat(
        self,
        message: str,
    ) -> AgentResult:

        from .executor import AgentExecutor

        context = ExecutionContext()

        context.variables.set(
            "message",
            message,
        )

        executor = AgentExecutor()

        return executor.execute(
            self,
            context,
        )

    def stream(
        self,
        message: str,
    ):

        from .executor import AgentExecutor

        context = ExecutionContext()

        context.variables.set(
            "message",
            message,
        )

        executor = AgentExecutor()

        return executor.stream(
            self,
            context,
        )

    #
    # Executable contract
    #

    def execute(
        self,
        context: ExecutionContext,
    ) -> AgentResult:

        from .executor import AgentExecutor

        executor = AgentExecutor()

        return executor.execute(
            self,
            context,
        )