from __future__ import annotations

from typing import TYPE_CHECKING

from .state import ExecutionState
from .step import ExecutionStep

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext

    from bindai_agent.agent import Agent


class ModelStep(ExecutionStep):
    """
    Executes the model call.
    """

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> None:

        state = context.data

        if not isinstance(
            state,
            ExecutionState,
        ):
            state = ExecutionState()
            context.data = state

        request = agent.conversation.to_request()

        response = agent.provider.complete(
            request,
        )

        state.request = request
        state.response = response
        state.iterations += 1

        return None
