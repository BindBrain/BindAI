# packages/bindai-agent/src/bindai_agent/execution/tool_execution_step.py

from __future__ import annotations

from typing import cast

from .state import ExecutionState
from .step import ExecutionStep


class ToolExecutionStep(
    ExecutionStep,
):
    """
    Executes every requested tool and appends
    tool results back into the conversation.
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

        response = state.response

        if response is None:
            return

        #
        # No tools requested.
        #

        if not response.tool_calls:
            return

        #
        # Store assistant tool-call message.
        #

        agent.conversation.add_assistant_tool_call(
            response.tool_calls,
        )

        #
        # Execute each tool.
        #

        for tool_call in response.tool_calls:

            result = agent.execute_tool(
                tool_call.name,
                **tool_call.arguments,
            )

            agent.conversation.add_tool(
                tool_call_id=tool_call.id,
                content=str(result.value),
            )

        #
        # Build the next request that includes
        # the tool outputs.
        #

        state.request = agent.conversation.to_request()

        #
        # Count another model iteration.
        #

        state.iterations += 1

        #
        # Continue the execution pipeline.
        #

        return None