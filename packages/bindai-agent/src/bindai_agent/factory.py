from __future__ import annotations

from .builder import AgentBuilder
from .loader import AgentLoader


def Agent(
    *,
    model: str = "gpt-4.1-mini",
    provider: str = "openai",
    instructions: str = "",
    tools=None,
    memory=None,
    knowledge=None,
):

    builder = AgentBuilder()

    builder.model(
        f"{provider}:{model}",
    )

    if instructions:
        builder.instructions(
            instructions,
        )

    if tools:
        builder.with_tools(
            *tools,
        )

    if memory:
        builder.with_memory(
            memory,
        )

    if knowledge:
        builder.with_knowledge(
            knowledge,
        )

    return builder.build()


# Attach helper after function is created
Agent.from_yaml = AgentLoader.from_yaml