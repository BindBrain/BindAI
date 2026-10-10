from __future__ import annotations

from .state import ExecutionState
from .step import ExecutionStep


class InitializationStep(
    ExecutionStep,
):

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

        if not isinstance(
            context.data,
            ExecutionState,
        ):
            context.data = ExecutionState()

        return None
