from __future__ import annotations

from bindai_memory import MemoryRecord


class MemoryStep:
    """
    Handles loading and saving
    long-term memory.
    """

    def load(
        self,
        agent,
    ) -> None:

        result = agent.memory.get(
            "__context__",
        )

        if not result.success:
            return

        record = result.value

        if record is None:
            return

        agent.conversation.add_system(
            f"Relevant memory:\n{record.value}",
        )

    def save(
        self,
        agent,
    ) -> None:

        transcript = []

        for message in agent.conversation.messages:

            transcript.append(
                f"{message.role.value}: {message.content}"
            )

        agent.memory.set(
            MemoryRecord(
                key="__context__",
                value="\n".join(
                    transcript,
                ),
            )
        )