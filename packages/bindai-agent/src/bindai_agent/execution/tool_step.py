from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .state import ExecutionState
from .step import ExecutionStep

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext

    from bindai_agent.agent import Agent


class ToolStep(ExecutionStep):
    """
    Executes model requested tools.
    """

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> None:

        state = context.data

        if not isinstance(
            state,
            ExecutionState,
        ):
            return None

        response = state.response

        if response is None:
            return None

        for tool_call in response.tool_calls:
            try:
                result: Any = agent.tools.execute(
                    tool_call.name,
                    **tool_call.arguments,
                )

            except Exception as ex:
                result = {
                    "error": str(ex),
                }

            agent.conversation.add_tool(
                tool_call_id=tool_call.name,
                content=str(result),
            )

        return None
