from __future__ import annotations

from bindai_core.context import ExecutionContext

from .agent import Agent
from .result import AgentResult


class AgentExecutor:
    """
    Executes an agent.
    """

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> AgentResult:

        return agent.execute(context)