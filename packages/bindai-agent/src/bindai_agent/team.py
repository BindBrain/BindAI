from __future__ import annotations

from .agent import Agent
from .result import AgentResult


class AgentTeam:
    """
    Collection of agents that can collaborate on a task.
    """

    def __init__(
        self,
        *,
        name: str,
    ) -> None:
        self.name = name
        self._agents: dict[str, Agent] = {}

    def add(
        self,
        agent: Agent,
    ) -> AgentTeam:
        self._agents[agent.name] = agent
        return self

    def get(
        self,
        name: str,
    ) -> Agent:
        return self._agents[name]

    def remove(
        self,
        name: str,
    ) -> None:
        self._agents.pop(name, None)

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

    def size(
        self,
    ) -> int:
        return len(self._agents)

    def run(
        self,
        message: str,
    ) -> AgentResult:
        """
        Run the task through each team agent sequentially.
        """

        results: dict[str, object] = {}

        for agent in self._agents.values():
            result = agent.run(message)

            if not result.success:
                return AgentResult(
                    success=False,
                    output=results,
                    error=result.error or f"Agent '{agent.name}' failed.",
                )

            results[agent.name] = result.output

        return AgentResult(
            success=True,
            output=results,
        )
