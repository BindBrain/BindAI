from __future__ import annotations

from typing import cast

from bindai_memory import MemoryRecord

from ..result import AgentResult
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

        state = cast(
            ExecutionState,
            context.data,
        )

        response = ""

        structured = None

        if state.response is not None:
            response = state.response.content or ""

            agent.conversation.add_assistant(
                response,
            )

            output_type = context.variables.get(
                "output_type",
            )

            if output_type is not None:
                try:
                    import json

                    data = json.loads(response)

                    structured = output_type(**data)

                except Exception:
                    structured = None

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

        result = AgentResult(
            success=True,
            output=structured if structured is not None else response,
        )

        #
        # Execute hooks
        #

        for hook in agent.hooks:
            hook(
                agent,
                context,
                result,
            )

        return result
