from typing import cast

from .state import ExecutionState
from .step import ExecutionStep


class ToolExecutionStep(ExecutionStep):
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

        if not response.tool_calls:
            return

        agent.conversation.add_assistant_tool_call(
            response.tool_calls,
        )

        for tool_call in response.tool_calls:
            result = agent.execute_tool(
                tool_call.name,
                context=context,
                **tool_call.arguments,
            )

            content = (
                str(result.value)
                if result.success
                else (
                    f"Tool execution failed: "
                    f"{result.error or 'Unknown error.'}"
                )
            )

            agent.conversation.add_tool(
                tool_call_id=tool_call.id,
                content=content,
            )

        state.request = agent.conversation.to_request()

        state.iterations += 1

        return None
