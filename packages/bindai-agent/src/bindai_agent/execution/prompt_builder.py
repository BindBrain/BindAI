from __future__ import annotations

from bindai_core.model import ModelRequest
from bindai_core.schema import SchemaSerializer


class PromptBuilder:
    """
    Responsible for constructing the
    ModelRequest sent to the provider.
    """

    def build(
        self,
        agent,
        context,
    ) -> ModelRequest:

        request = agent.conversation.to_request()

        request.tools = agent.tools.definitions()

        output_type = context.variables.get(
            "output_type",
        )

        if output_type is not None:

            request.response_schema = (
                SchemaSerializer.serialize(
                    output_type,
                )
            )

        #
        # Store the generated request
        # inside the execution context.
        #

        if context.data is not None:

            context.data.request = request

        return request