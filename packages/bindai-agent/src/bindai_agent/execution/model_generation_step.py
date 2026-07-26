from __future__ import annotations

from typing import cast

from bindai_core.events import (
    ModelRequestEvent,
    ModelResponseEvent,
)

from .state import ExecutionState
from .step import ExecutionStep


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

        state = cast(
            ExecutionState,
            context.data,
        )

        #
        # Publish request event.
        #

        agent.events.publish(
            ModelRequestEvent(
                request=state.request,
            )
        )

        #
        # Generate model response.
        #

        if state.streaming:

            state.response = agent.provider.generate_stream(
                state.request,
            )

        else:

            state.response = agent.provider.generate(
                state.request,
            )

        #
        # Publish response event.
        #

        agent.events.publish(
            ModelResponseEvent(
                response=state.response,
            )
        )

        #
        # Continue pipeline.
        #

        return None