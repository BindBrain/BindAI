from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_agent import Agent, AgentResult


@dataclass(slots=True)
class Task:
    """
    A single unit of work executed by an Agent.
    """

    description: str

    agent: Agent

    expected_output: str | None = None

    context: list[Task] = field(
        default_factory=list,
    )

    result: AgentResult | None = None

    def context_from(
        self,
        *tasks: Task,
    ) -> Task:

        self.context.extend(
            tasks,
        )

        return self
