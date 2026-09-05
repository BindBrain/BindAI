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
        self._roles: dict[str, Agent] = {}

    def add(
        self,
        agent: Agent,
        *,
        role: str | None = None,
    ) -> AgentTeam:
        self._agents[agent.name] = agent

        if role is not None:
            self._roles[role] = agent

        return self

    def get(
        self,
        name: str,
    ) -> Agent:
        return self._agents[name]

    def role(
        self,
        role: str,
    ) -> Agent:
        return self._roles[role]

    def roles(
        self,
    ) -> list[str]:
        return list(self._roles.keys())

    def run_role(
        self,
        role: str,
        message: str,
    ) -> AgentResult:
        agent = self.role(role)
        return agent.run(message)

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

    def run_parallel_then_review(
        self,
        message: str,
    ) -> AgentResult:
        """
        Run all agents except the final agent in parallel,
        then pass their combined outputs to the final agent for review.
        """

        agents = self.all()

        if not agents:
            return AgentResult(
                success=False,
                error="AgentTeam has no agents.",
            )

        if len(agents) == 1:
            result = agents[0].run(message)

            return AgentResult(
                success=result.success,
                output=result.output,
                error=result.error,
            )

        specialists = agents[:-1]
        reviewer = agents[-1]

        with ThreadPoolExecutor(max_workers=len(specialists)) as executor:
            futures = {
                agent.name: executor.submit(agent.run, message)
                for agent in specialists
            }

            outputs: dict[str, object] = {}

            for name, future in futures.items():
                result = future.result()

                if not result.success:
                    return AgentResult(
                        success=False,
                        output=outputs,
                        error=result.error or f"Agent '{name}' failed.",
                    )

                outputs[name] = result.output

        review_message = "\n".join(
            f"{name}: {output}"
            for name, output in outputs.items()
        )

        result = reviewer.run(review_message)

        if not result.success:
            return AgentResult(
                success=False,
                output=outputs,
                error=result.error or f"Agent '{reviewer.name}' failed.",
            )

        return AgentResult(
            success=True,
            output=result.output,
        )
