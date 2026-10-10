from __future__ import annotations

from pathlib import Path
from typing import Any

from bindai_config.tool_loader import ToolLoader

from ..builder import AgentBuilder
from ..registry import AgentRegistry
from .models import AgentDefinition


def build_agent(
    definition: AgentDefinition,
    *,
    project_root: str | Path | None = None,
    tools: dict[str, Any] | None = None,
    memory: Any | None = None,
    retriever: Any | None = None,
    knowledge: Any | None = None,
    middleware: dict[str, Any] | None = None,
    hooks: dict[str, Any] | None = None,
):
    """
    Build and register a real BindAI agent from a declarative definition.

    ``definition.id`` is the stable Studio/resource identifier. The runtime
    Agent keeps its human-readable ``definition.name`` and is additionally
    registered under the definition ID so workflow AgentNodes can reference
    the portable resource ID.
    """
    if project_root is not None:
        root = Path(project_root).expanduser().resolve()
        builder = AgentBuilder().from_project(root)

        if tools is None:
            loaded_tools = ToolLoader.load(root)
            tools = {
                tool.name: tool
                for tool in loaded_tools
                if hasattr(tool, "name")
            }
    else:
        builder = AgentBuilder()

    builder.name(definition.name)

    if definition.provider and definition.model:
        builder.model(
            f"{definition.provider}:{definition.model}",
            connection=definition.connection,
        )
    elif definition.provider or definition.model:
        raise ValueError(
            f"Agent '{definition.id}' must define both provider and model."
        )

    if definition.instructions:
        builder.instructions(definition.instructions)

    if definition.temperature is not None:
        builder.temperature(definition.temperature)

    if definition.max_tokens is not None:
        builder.max_tokens(definition.max_tokens)

    builder.max_tool_iterations(definition.max_tool_iterations)

    if definition.tools:
        if tools is None:
            raise ValueError(
                f"Agent '{definition.id}' references tools but no tool registry "
                "was provided."
            )

        for tool_name in definition.tools:
            if tool_name not in tools:
                raise ValueError(
                    f"Agent '{definition.id}' references unknown tool "
                    f"'{tool_name}'."
                )

            builder.tools(tools[tool_name])

    if definition.memory is not None:
        if memory is None:
            raise ValueError(
                f"Agent '{definition.id}' references memory "
                f"'{definition.memory}', but no memory resource was provided."
            )
        builder.memory(memory)

    if definition.retriever is not None:
        if retriever is None:
            raise ValueError(
                f"Agent '{definition.id}' references retriever "
                f"'{definition.retriever}', but no retriever resource was "
                "provided."
            )
        builder.retriever(retriever)

    if definition.knowledge is not None:
        if knowledge is None:
            raise ValueError(
                f"Agent '{definition.id}' references knowledge "
                f"'{definition.knowledge}', but no knowledge resource was "
                "provided."
            )
        builder.knowledge(knowledge)

    if definition.middleware:
        if middleware is None:
            raise ValueError(
                f"Agent '{definition.id}' references middleware but no "
                "middleware registry was provided."
            )

        for middleware_name in definition.middleware:
            if middleware_name not in middleware:
                raise ValueError(
                    f"Agent '{definition.id}' references unknown middleware "
                    f"'{middleware_name}'."
                )

            builder.middleware(middleware[middleware_name])

    if definition.hooks:
        if hooks is None:
            raise ValueError(
                f"Agent '{definition.id}' references hooks but no hook "
                "registry was provided."
            )

        for hook_name in definition.hooks:
            if hook_name not in hooks:
                raise ValueError(
                    f"Agent '{definition.id}' references unknown hook "
                    f"'{hook_name}'."
                )

            builder.hook(hooks[hook_name])

    agent = builder.build()

    if definition.id != agent.name:
        AgentRegistry.register_alias(
            definition.id,
            agent,
        )

    return agent
