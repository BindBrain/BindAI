from bindai_core.model import ModelRequest

from .state import ExecutionState
from .step import ExecutionStep


class ModelRequestStep(
    ExecutionStep,
):

    def execute(
        self,
        agent,
        context,
    ):

        state = context.data

        state.request = ModelRequest(
            messages=agent.conversation.messages,
            tools=agent.tools.definitions(),
        )

        return None
