from __future__ import annotations

from .step import ExecutionStep


class InitializationStep(
    ExecutionStep,
):

    def execute(
        self,
        agent,
        context,
    ):

        user_input = context.variables.get(
            "input",
            "",
        )

        if len(
            agent.conversation
        ) == 0:

            agent.conversation.add_system(
                agent.instructions,
            )

        agent.conversation.add_user(
            user_input,
        )