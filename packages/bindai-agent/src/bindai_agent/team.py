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

    def run_roles(
        self,
        roles: list[str],
        message: str,
    ) -> AgentResult:
        results: dict[str, object] = {}

        for role in roles:
            result = self.run_role(role, message)

            if not result.success:
                return AgentResult(
                    success=False,
                    output=results,
                    error=result.error or f"Role '{role}' failed.",
                )

            results[role] = result.output

        return AgentResult(
            success=True,
            output=results,
        )

    def run_roles_chain(
        self,
        roles: list[str],
        message: str,
    ) -> AgentResult:
        """
        Run selected roles sequentially, passing each role's
        output to the next role.
        """

        current_message = message

        for role in roles:
            result = self.run_role(
                role,
                current_message,
            )

            if not result.success:
                return AgentResult(
                    success=False,
                    output=current_message,
                    error=result.error or f"Role '{role}' failed.",
                )

            current_message = str(result.output)

        return AgentResult(
            success=True,
            output=current_message,
        )

    def run_roles_parallel(
        self,
        roles: list[str],
        message: str,
    ) -> AgentResult:
        selected_agents = {role: self.role(role) for role in roles}

        with ThreadPoolExecutor(max_workers=len(selected_agents)) as executor:
            futures = {
                role: executor.submit(agent.run, message) for role, agent in selected_agents.items()
            }

            results: dict[str, object] = {}

            for role, future in futures.items():
                result = future.result()

                if not result.success:
                    return AgentResult(
                        success=False,
                        output=results,
                        error=result.error or f"Role '{role}' failed.",
                    )

                results[role] = result.output

        return AgentResult(
            success=True,
            output=results,
        )

    def remove(
        self,
        name: str,
    ) -> None:
        agent = self._agents.pop(name, None)

        if agent is None:
            return

        roles_to_remove = [role for role, role_agent in self._roles.items() if role_agent is agent]

        for role in roles_to_remove:
            del self._roles[role]

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
        self._roles.clear()

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

    def run_continue(
        self,
        message: str,
    ) -> AgentResult:
        """
        Run all team agents and continue even when an agent fails.
        """

        results: dict[str, object] = {}
        errors: list[str] = []

        for agent in self._agents.values():
            result = agent.run(message)

            if result.success:
                results[agent.name] = result.output
            else:
                results[agent.name] = None
                errors.append(f"{agent.name}: {result.error or 'Agent execution failed.'}")

        if errors:
            return AgentResult(
                success=False,
                output=results,
                error="\n".join(errors),
            )

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
                agent.name: executor.submit(agent.run, message) for agent in self._agents.values()
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
            futures = {agent.name: executor.submit(agent.run, message) for agent in specialists}

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

        review_message = "\n".join(f"{name}: {output}" for name, output in outputs.items())

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
