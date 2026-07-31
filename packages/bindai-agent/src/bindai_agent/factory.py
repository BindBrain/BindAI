from __future__ import annotations

from pathlib import Path

from bindai_config.runtime import ProjectRuntime

from .builder import AgentBuilder
from .loader import AgentLoader


def create_agent(
    *,
    model: str | None = None,
    provider: str | None = None,
    instructions: str = "",
    tools=None,
    memory=None,
    knowledge=None,
):

    #
    # Load project configuration
    #

    runtime = ProjectRuntime(
        Path.cwd(),
    )

    config = runtime.config

    #
    # Create builder
    #

    builder = AgentBuilder()

    #
    # Model / Provider
    #

    builder.model(
        f"{provider or config.provider}:{model or config.model}",
    )

    #
    # Temperature
    #

    builder.temperature(
        config.temperature,
    )

    #
    # Instructions
    #

    if instructions:
        builder.instructions(
            instructions,
        )

    #
    # Components
    #

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

    #
    # Build
    #

    return builder.build()


#
# Convenience loader
#

def create_agent_from_yaml(path):
    return AgentLoader.from_yaml(path)
