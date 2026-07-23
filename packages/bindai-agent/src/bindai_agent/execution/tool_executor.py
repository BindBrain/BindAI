from __future__ import annotations

from typing import Any, cast

from .step import ExecutionStep
from .state import ExecutionState


class ToolExecutor(
    ExecutionStep,
):
    """
    Executes model tool calls.
    """

    def execute(
        self,
        agent,
        context,
    ):

        state = cast(ExecutionState, context.data)

        response = state.response

        if response is None or not response.tool_calls:
            return

        agent.conversation.add_assistant_tool_call(
            response.tool_calls,
        )

        for tool_call in response.tool_calls:

            for hook in cast(list[Any], agent.hooks):
                hook.on_tool_start(
                    tool_call,
                )

            result = agent.execute_tool(
                tool_call.name,
                **tool_call.arguments,
            )

            for hook in cast(list[Any], agent.hooks):
                hook.on_tool_end(
                    tool_call,
                    result,
                )

            agent.conversation.add_tool(
                tool_call_id=tool_call.id,
                content=(
                    str(result.output)
                    if result.success
                    else f"ERROR: {result.error}"
                ),
            )

        return response