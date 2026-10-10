from __future__ import annotations

from bindai_core.model import ModelRequest

from .state import ExecutionState
from .step import ExecutionStep


class RequestBuildStep(
    ExecutionStep,
):
    """
    Builds final model request after
    all context enrichment.
    """

    def execute(
        self,
        agent,
        context,
    ):

        state = context.data

        if not isinstance(
            state,
            ExecutionState,
        ):
            state = ExecutionState()

        configuration = agent.configuration

        state.request = ModelRequest(
            messages=list(
                agent.conversation.messages,
            ),
            temperature=configuration.temperature,
            max_tokens=configuration.max_tokens,
            tools=agent.tools.definitions(),
        )

        context.data = state
