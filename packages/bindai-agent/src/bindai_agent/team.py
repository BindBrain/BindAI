from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

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

    def test_agent_team_chain_stops_when_agent_fails():
        from bindai_agent import AgentResult

        class ChainAgent:
            def __init__(self, name, output=None, error=None):
                self.name = name
                self.output = output
                self.error = error
                self.received_message = None

            def run(self, message):
                self.received_message = message

                if self.error:
                    return AgentResult(success=False, error=self.error)

                return AgentResult(success=True, output=self.output)

        first = ChainAgent("Researcher", output="Research complete.")
        second = ChainAgent("Writer", error="Writer failed.")
        third = ChainAgent("Reviewer", output="Review complete.")

        team = AgentTeam(name="Content Team")
        team.add(first).add(second).add(third)

        result = team.run_chain("Create an article.")

        assert result.success is False
        assert result.error == "Writer failed."
        assert result.output == "Research complete."
        assert third.received_message is None

    def run_chain(
        self,
        message: str,
    ) -> AgentResult:
        """
        Run the task through each team agent sequentially,
        passing each agent's output to the next agent.
        """

        current_message = message

        for agent in self._agents.values():
            result = agent.run(current_message)

            if not result.success:
                return AgentResult(
                    success=False,
                    output=current_message,
                    error=result.error or f"Agent '{agent.name}' failed.",
                )

            current_message = str(result.output)

        return AgentResult(
            success=True,
            output=current_message,
        )

    def run_parallel(
        self,
        message: str,
    ) -> AgentResult:
        """
        Run the task through all team agents in parallel.
        """

        with ThreadPoolExecutor(max_workers=self.size()) as executor:
            futures = {
                agent.name: executor.submit(agent.run, message)
                for agent in self._agents.values()
            }

            results: dict[str, object] = {}

            for name, future in futures.items():
                result = future.result()

                if not result.success:
                    return AgentResult(
                        success=False,
                        output=results,
                        error=result.error or f"Agent '{name}' failed.",
                    )

                results[name] = result.output

        return AgentResult(
            success=True,
            output=results,
        )
