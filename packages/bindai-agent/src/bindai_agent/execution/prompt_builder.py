from __future__ import annotations

from bindai_core.model import ModelRequest
from bindai_core.schema import SchemaSerializer

from .state import ExecutionState


class PromptBuilder:
    """
    Builds the ModelRequest for the provider.
    """

    def build(
        self,
        agent,
        context,
    ) -> ModelRequest:

        state: ExecutionState = context.data

        request = agent.conversation.to_request()

        request.tools = agent.tools.definitions()

        output_type = context.variables.get(
            "output_type",
        )

        if output_type is not None:
            request.response_schema = SchemaSerializer.serialize(
                output_type,
            )

        state.request = request

        return request
