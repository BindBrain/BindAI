from __future__ import annotations

from ..output.parser import OutputParser
from ..result import AgentResult


class FinishStep:
    """
    Finalizes an agent execution.
    """

    def finish(
        self,
        agent,
        context,
        response,
        memory_step,
    ) -> AgentResult:

        #
        # Save assistant message
        #

        agent.conversation.add_assistant(
            response.content,
        )

        #
        # Persist memory
        #

        memory_step.save(
            agent,
        )

        #
        # Structured output
        #

        output_type = context.variables.get(
            "output_type",
        )

        output = OutputParser.parse(
            response.content,
            output_type,
        )

        result = AgentResult(
            success=True,
            output=output,
        )

        #
        # Hooks
        #

        for hook in agent.hooks:

            hook.on_finish(
                result,
            )

        return result