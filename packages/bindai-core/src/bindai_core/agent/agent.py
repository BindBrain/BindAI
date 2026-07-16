from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable
from bindai_core.model import ModelProvider

from .configuration import AgentConfiguration
from .result import AgentResult
from .state import AgentState

from bindai_core.conversation import Conversation


class Agent(Executable, ABC):
    """
    Base class for every BindAI agent.
    """

    def __init__(
        self,
        name: str,
        instructions: str,
        provider: ModelProvider,
    ):
        self.configuration = AgentConfiguration()

        self.configuration.name = name
        self.configuration.instructions = instructions

        self.provider = provider
        self.conversation = Conversation()
        self.state = AgentState.IDLE

    @property
    def name(self) -> str:
        return self.configuration.name

    @property
    def instructions(self) -> str:
        return self.configuration.instructions

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext,
    ) -> AgentResult:
        """
        Execute the agent.
        """
        ...