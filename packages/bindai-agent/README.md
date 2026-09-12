# BindAI Agent

`bindai-agent` provides the agent layer of the BindAI framework.

It contains the core abstractions for creating, configuring, executing, and coordinating AI agents, including agent builders, configuration, state, delegation, registries, and agent teams.

## Features

* Agent creation and execution
* Structured agent configuration
* Agent builders
* Agent state management
* Agent registries
* Agent delegation
* Agent teams and team delegation
* Assistant agents
* YAML-based agent creation
* Agent execution results

## Public API

The package exposes the following primary components:

```python
from bindai_agent import (
    Agent,
    AssistantAgent,
    AgentBuilder,
    AgentConfiguration,
    AgentDelegationTool,
    AgentRegistry,
    AgentResult,
    AgentState,
    AgentTeam,
    AgentTeamDelegationTool,
    create_agent,
    create_agent_from_yaml,
)
```

## Basic Usage

Agents can be created using the builder API:

```python
from bindai_agent import Agent

agent = Agent.builder().name("assistant").instructions("You are a helpful AI assistant.").build()

result = agent.run("Explain what BindAI is.")

print(result.output)
```

## Factory Functions

The package also provides factory functions for creating agents:

```python
from bindai_agent import create_agent

agent = create_agent(
    name="assistant",
    instructions="You are a helpful AI assistant.",
)
```

Agents can also be created from YAML configuration:

```python
from bindai_agent import create_agent_from_yaml

agent = create_agent_from_yaml("agent.yaml")
```

## Agent Delegation

Agents can delegate work to other agents through the delegation APIs provided by the package.

```python
from bindai_agent import Agent, AgentDelegationTool

# Agent delegation capabilities are provided by the
# BindAI agent execution system.
```

For more advanced delegation and coordination patterns, see the BindAI documentation.

## Agent Teams

`AgentTeam` and `AgentTeamDelegationTool` provide the foundation for coordinating multiple agents as part of a team.

```python
from bindai_agent import AgentTeam
```

Agent teams are part of BindAI's broader multi-agent architecture.

## Architecture

`bindai-agent` sits above the lower-level BindAI core components and provides the agent-specific execution layer.

Conceptually:

```text
BindAI
  │
  ├── bindai-agent
  │     ├── Agents
  │     ├── Agent configuration
  │     ├── Agent state
  │     ├── Delegation
  │     └── Agent teams
  │
  └── BindAI Core
        ├── Execution
        ├── Context
        ├── Events
        └── Tools
```

The main `bindai` package builds on this agent layer together with the other BindAI components.

## Documentation

For complete framework documentation, visit the BindAI documentation:

https://docs.bindai.dev

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash
uv sync
uv run pytest
```

To run the agent package tests specifically:

```bash
uv run pytest packages/bindai-agent/tests -q
```

## License

BindAI is released under the MIT License.
