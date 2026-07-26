from __future__ import annotations

from .agent import Agent


class AgentRegistry:
    """
    Global registry of application agents.
    """

    _agents: dict[str, Agent] = {}

    @classmethod
    def register(
        cls,
        agent: Agent,
    ) -> None:

        cls._agents[agent.name] = agent

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Agent:

        return cls._agents[name]

    @classmethod
    def remove(
        cls,
        name: str,
    ) -> None:

        cls._agents.pop(name, None)

    @classmethod
    def contains(
        cls,
        name: str,
    ) -> bool:

        return name in cls._agents

    @classmethod
    def names(
        cls,
    ) -> list[str]:

        return list(cls._agents.keys())

    @classmethod
    def all(
        cls,
    ) -> list[Agent]:

        return list(cls._agents.values())

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._agents.clear()

    @classmethod
    def size(
        cls,
    ) -> int:

        return len(cls._agents)