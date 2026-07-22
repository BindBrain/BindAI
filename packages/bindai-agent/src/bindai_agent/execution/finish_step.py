from __future__ import annotations

from bindai_memory import MemoryRecord

from .result import ExecutionResult
from .state import ExecutionState
from .step import ExecutionStep


class FinishStep(
    ExecutionStep,
):
    """
    Finalizes execution.
    """

    def execute(
        self,
        agent,
        context,
    ):

        state: ExecutionState = context.data

        response = None

        #
        # Store assistant message
        #

        if state.response is not None:
            response = state.response.content

            agent.conversation.add_assistant(
                response,
            )

        #
        # Persist conversation memory
        #

        if agent.memory is not None:
            transcript = "\n".join(
                f"{message.role.value}: {message.content}"
                for message in agent.conversation.messages
            )

            agent.memory.set(
                MemoryRecord(
                    key="__context__",
                    value=transcript,
                )
            )

        result = ExecutionResult(
            success=True,
            response=response,
            iterations=state.iterations,
        )

        #
        # Middleware (after)
        #

        return result
