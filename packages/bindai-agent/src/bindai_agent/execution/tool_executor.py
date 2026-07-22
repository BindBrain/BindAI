from __future__ import annotations


class ToolExecutor:
    """
    Executes tool calls and
    appends results back into
    the conversation.
    """

    def execute(
        self,
        agent,
        response,
    ) -> None:

        agent.conversation.add_assistant_tool_call(
            response.tool_calls,
        )

        for tool_call in response.tool_calls:

            #
            # Hooks before execution
            #

            for hook in agent.hooks:

                hook.on_tool_start(
                    tool_call,
                )

            result = agent.execute_tool(
                tool_call.name,
                **tool_call.arguments,
            )

            #
            # Hooks after execution
            #

            for hook in agent.hooks:

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