from __future__ import annotations

from bindai_core.model import ModelRequest

from .state import ExecutionState
from .step import ExecutionStep


class InitializationStep(
    ExecutionStep,
):
    """
    Initializes execution state.
    """

    def execute(
        self,
        agent,
        context,
    ):

        user_input = context.variables.get(
            "input",
            "",
        )

        if len(agent.conversation) == 0:
            agent.conversation.add_system(
                agent.instructions,
            )

        agent.conversation.add_user(
            user_input,
        )

        state = ExecutionState()

        state.request = ModelRequest(
            messages=agent.conversation.messages,
        )

        context.data = state

        return None