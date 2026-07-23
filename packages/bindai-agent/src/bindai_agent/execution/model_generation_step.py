from __future__ import annotations

from .step import ExecutionStep
from .state import ExecutionState
from typing import cast

class ModelGenerationStep(
    ExecutionStep,
):
    """
    Calls the provider and stores the response.
    """

    def execute(
        self,
        agent,
        context,
    ):

        state = cast(ExecutionState, context.data)

        state.response = agent.provider.generate(
            state.request,
        )

        #
        # Continue pipeline.
        #

        return None
