from __future__ import annotations

from bindai_memory import MemoryRecord

from .step import ExecutionStep


class MemoryStep(
    ExecutionStep,
):
    """
    Loads long-term memory before execution
    and saves it after execution.
    """

    def execute(
        self,
        agent,
        context,
    ):

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
    ):

        transcript = []

        for message in agent.conversation.messages:
            transcript.append(f"{message.role.value}: {message.content}")

        agent.memory.set(
            MemoryRecord(
                key="__context__",
                value="\n".join(
                    transcript,
                ),
            )
        )
