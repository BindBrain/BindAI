from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AgentConfig:

    id: str

    name: str

    instructions: str

    provider: str = "openai"

    model: str = "gpt-4.1"

    temperature: float = 0.7

    max_tokens: int | None = None


@dataclass(slots=True)
class TaskConfig:

    id: str

    description: str

    agent: str

    expected_output: str | None = None

    context: list[str] = field(
        default_factory=list,
    )


@dataclass(slots=True)
class GroupConfig:

    name: str

    process: str = "sequential"

    description: str = ""

    agents: list[AgentConfig] = field(
        default_factory=list,
    )

    tasks: list[TaskConfig] = field(
        default_factory=list,
    )