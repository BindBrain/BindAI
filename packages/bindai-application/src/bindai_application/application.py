from __future__ import annotations

from bindai_agent import Agent

from .configuration import ApplicationConfiguration


class Application:
    """
    Represents a business application inside a project.

    Examples:

        HR
        Finance
        Fleet
        Procurement
    """

    def __init__(
        self,
        configuration: ApplicationConfiguration,
    ):

        self.configuration = configuration

        self.agents: dict[str, Agent] = {}

        #
        # Future
        #

        self.workflows = {}

        self.knowledge = {}

        self.memories = {}

    @property
    def name(
        self,
    ) -> str:

        return self.configuration.name

    #
    # Agents
    #

    def add_agent(
        self,
        agent: Agent,
    ):

        self.agents[agent.name] = agent

        return self

    def agent(
        self,
        name: str,
    ) -> Agent:

        return self.agents[name]

    #
    # Execution
    #

    def run(
        self,
        *,
        agent: str,
        message: str,
    ):

        return self.agent(
            agent,
        ).chat(
            message,
        )

    def stream(
        self,
        *,
        agent: str,
        message: str,
    ):

        return self.agent(
            agent,
        ).stream(
            message,
        )

    #
    # Python Helpers
    #

    def __contains__(
        self,
        name: str,
    ):

        return name in self.agents

    def __len__(
        self,
    ):

        return len(self.agents)

    def __iter__(
        self,
    ):

        return iter(self.agents.values())
