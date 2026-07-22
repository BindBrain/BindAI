from __future__ import annotations

from .step import ExecutionStep
from .state import ExecutionState


class ToolLoop(
    ExecutionStep,
):
    """
    Executes tool calls until
    the model stops requesting tools.
    """

    def execute(
        self,
        agent,
        context,
    ):

        state: ExecutionState = context.data

        while True:
            response = state.response

            #
            # No tool calls
            #

            if response is None or not getattr(
                response,
                "tool_calls",
                None,
            ):
                return

            #
            # Execute tools
            #

            for call in response.tool_calls:
                result = agent.tool_executor.execute(
                    call,
                )

                agent.conversation.add_tool(
                    call.id,
                    str(result),
                )

            #
            # Ask model again
            #

            state.response = agent.provider.generate(
                state.request,
            )
