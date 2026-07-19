from __future__ import annotations

from .agent import Agent


class AgentRegistry:
    """
    Registry of application agents.
    """

    def __init__(self):

        self._agents: dict[str, Agent] = {}

    def register(
        self,
        agent: Agent,
    ) -> None:

        self._agents[agent.name] = agent

    def get(
        self,
        name: str,
    ) -> Agent:

        return self._agents[name]

    def remove(
        self,
        name: str,
    ) -> None:

        del self._agents[name]

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._agents

    def names(
        self,
    ) -> list[str]:

        return list(self._agents.keys())

    def all(
        self,
    ) -> list[Agent]:

        return list(self._agents.values())

    def clear(
        self,
    ) -> None:

        self._agents.clear()

    def __len__(self):

        return len(self._agents)