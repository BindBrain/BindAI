from __future__ import annotations

from .step import ExecutionStep


class KnowledgeStep(
    ExecutionStep,
):
    """
    Inject retrieved knowledge into the conversation.
    """

    def execute(
        self,
        agent,
        context,
    ):

        #
        # New Retrieval API
        #

        if agent.retriever is not None:
            result = agent.retriever.retrieve(
                context.variables.get(
                    "input",
                    "",
                )
            )

            documents = result.documents

        #
        # Backward compatibility
        #

        elif agent.knowledge is not None:
            result = agent.knowledge.search(
                context.variables.get(
                    "input",
                    "",
                )
            )

            if not result.success:
                return

            documents = result.value or []

        else:
            return

        if not documents:
            return

        content = "\n\n".join(
            getattr(doc, "content", getattr(doc, "value", "")) for doc in documents
        )

        agent.conversation.add_system(
            f"Relevant knowledge:\n{content}",
        )
