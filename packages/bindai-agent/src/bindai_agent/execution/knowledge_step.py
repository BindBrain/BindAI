from __future__ import annotations


class KnowledgeStep:
    """
    Handles retrieval of relevant
    knowledge before model inference.
    """

    def inject(
        self,
        agent,
        query: str,
    ) -> None:

        if agent.knowledge is None:
            return

        context = agent.knowledge.retrieve(
            query,
        )

        if not context:
            return

        agent.conversation.add_system(
            f"Relevant knowledge:\n{context}"
        )