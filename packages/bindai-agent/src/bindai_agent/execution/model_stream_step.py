from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from .state import ExecutionState
from .step import ExecutionStep

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext

    from bindai_agent.agent import Agent


class ModelStreamStep(ExecutionStep):
    """
    Executes streaming model generation.
    """

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> Iterator:

        state = context.data

        if not isinstance(
            state,
            ExecutionState,
        ):
            return iter(())

        stream: Iterator = agent.provider.stream(
            state.request,
        )

        return stream
