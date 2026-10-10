from bindai_agent import Agent, AgentRegistry
from bindai_model import ModelRegistry


class ApplicationAgentRegistry:
    def __init__(self):
        self._agents: dict[str, Agent] = {}

    def register(
        self,
        agent: Agent,
    ) -> None:
        self._agents[agent.name] = agent

    def register_alias(
        self,
        name: str,
        agent: Agent,
    ) -> None:
        if not name:
            raise ValueError(
                "Agent registry alias cannot be empty."
            )

        self._agents[name] = agent

    def get(
        self,
        name: str,
    ) -> Agent:
        return self._agents[name]

    def remove(
        self,
        name: str,
    ) -> None:
        self._agents.pop(
            name,
            None,
        )

    def contains(
        self,
        name: str,
    ) -> bool:
        return name in self._agents

    def names(
        self,
    ) -> list[str]:
        return list(
            self._agents.keys(),
        )

    def all(
        self,
    ) -> list[Agent]:
        return list(
            self._agents.values(),
        )

    def clear(self) -> None:
        self._agents.clear()

    def size(self) -> int:
        return len(
            self._agents,
        )

    def __len__(self) -> int:
        return len(
            self._agents,
        )


class ApplicationRegistry:
    def __init__(self):
        self.models = ModelRegistry()
        self.agents = ApplicationAgentRegistry()
