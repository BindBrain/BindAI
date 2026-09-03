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

        user_input = str(
            context.variables.get(
                "input",
                "",
            )
        )

        if len(agent.conversation) == 0:
            if agent.instructions:
                agent.conversation.add_system(
                    agent.instructions,
                )

        agent.conversation.add_user(
            user_input,
        )

        state = context.data

        if not isinstance(
            state,
            ExecutionState,
        ):
            state = ExecutionState()

        state.request = ModelRequest(
            messages=agent.conversation.messages,
            tools=agent.tools.definitions(),
        )

        context.data = state

        return None
