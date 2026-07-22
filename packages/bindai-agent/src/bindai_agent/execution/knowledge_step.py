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

        if agent.knowledge is None:
            return

        user_input = context.variables.get(
            "input",
            "",
        )

        result = agent.knowledge.search(
            user_input,
        )

        if not result.success:
            return

        documents = result.value or []

        if not documents:
            return

        content = "\n\n".join(
            doc.content
            for doc in documents
        )

        agent.conversation.add_system(
            f"Relevant knowledge:\n{content}",
        )