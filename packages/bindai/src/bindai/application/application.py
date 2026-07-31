from __future__ import annotations

from bindai_agent import Agent
from bindai_core.model import ModelProvider

from .configuration import ApplicationConfiguration
from .registry import ApplicationRegistry
from .state import ApplicationState


class Application:
    """
    Root BindAI application.
    """

    def __init__(
        self,
        configuration: ApplicationConfiguration | None = None,
    ):

        self._configuration = configuration or ApplicationConfiguration()

        self._registry = ApplicationRegistry()

        self._state = ApplicationState.CREATED

    @property
    def configuration(
        self,
    ) -> ApplicationConfiguration:

        return self._configuration

    @property
    def state(
        self,
    ) -> ApplicationState:

        return self._state

    @property
    def providers(
        self,
    ):

        return self._registry.providers

    @property
    def agents(
        self,
    ):

        return self._registry.agents

    def add_provider(
        self,
        provider: ModelProvider,
    ) -> Application:

        self.providers.register(
            provider,
        )

        return self

    def add_agent(
        self,
        agent: Agent,
    ) -> Application:

        self.agents.register(
            agent,
        )

        return self

    def initialize(
        self,
    ) -> None:

        self._state = ApplicationState.INITIALIZED

    def run(
        self,
    ) -> None:

        self._state = ApplicationState.RUNNING

    def stop(
        self,
    ) -> None:

        self._state = ApplicationState.STOPPED

    def chat(
        self,
        message: str,
    ):
        """
        Chat with the default agent.
        """

        if len(self.agents) == 0:
            raise RuntimeError("No agents registered.")

        agent = self.agents.all()[0]

        return agent.chat(
            message,
        )
