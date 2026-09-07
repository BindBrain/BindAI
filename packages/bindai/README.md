<p align="center">
  <a href="https://bindai.dev">
    <img src="logo/light.png" alt="BindAI Logo" width="220">
  </a>
</p>

<h1 align="center">BindAI</h1>

<p align="center">
  <strong>Build AI applications with agents, tools, workflows, memory, knowledge, and retrieval.</strong>
</p>

<p align="center">
  A modular Python framework for building AI applications from assistants and RAG systems to automation and multi-agent workflows.
</p>

<p align="center">
  <a href="https://docs.bindai.dev"><strong>Documentation</strong></a> Â·
  <a href="https://bindai.dev"><strong>Website</strong></a> Â·
  <a href="https://pypi.org/project/bindai/"><strong>PyPI</strong></a> Â·
  <a href="https://github.com/BindBrain/BindAI"><strong>GitHub</strong></a>
</p>

---

# Overview

BindAI is an open-source Python framework for building AI applications from composable components.

The framework brings together:

* AI agents
* Model providers
* Tool calling
* Workflows
* Memory
* Knowledge and RAG
* Embeddings
* Retrieval
* Multi-agent delegation and teams
* External connections
* MCP integration
* CLI and project configuration

The architecture is modular, so applications can start with a simple agent and grow into more sophisticated AI systems without requiring a completely different application structure.

---

# Installation

Install the main framework package:

```bash
pip install bindai
```

The BindAI ecosystem also provides separate packages for providers and integrations.

For development from the repository:

```bash
git clone https://github.com/BindBrain/BindAI.git

cd BindAI

uv sync
```

The repository root is a uv workspace. The root workspace itself is not installed with `pip install -e .`.

---

# Quick Start

The recommended programmatic construction API is `Agent.builder()`:

```python
from bindai import Agent

agent = (
    Agent.builder()
    .name("assistant")
    .instructions("You are a helpful AI assistant.")
    .provider("openai", model="gpt-4.1-mini")
    .build()
)

result = agent.run("Explain what BindAI is.")

print(result.output)
```

Provider/model selection can also use the `provider:model` format:

```python
from bindai import Agent

agent = (
    Agent.builder()
    .name("assistant")
    .instructions("You are a helpful AI assistant.")
    .model("openai:gpt-4.1-mini")
    .build()
)
```

Set the required provider environment variable before running the application.

For example:

```bash
OPENAI_API_KEY=your-key
```

See the documentation for provider-specific configuration and additional providers.

---

# Core Capabilities

## Agents

BindAI agents provide the primary runtime abstraction for AI application logic.

Agents support:

* Instructions and prompts
* Model providers
* Tool calling
* Structured output
* Streaming
* Memory
* Knowledge and retrieval
* Middleware
* Hooks and events
* Agent delegation
* Multi-agent teams
* Workflow integration

Example:

```python
from bindai import Agent

agent = (
    Agent.builder()
    .name("researcher")
    .instructions("You are a research assistant.")
    .model("openai:gpt-4.1-mini")
    .build()
)

result = agent.run("Explain retrieval-augmented generation.")

print(result.output)
```

---

## Tools

Tools allow agents to call application-defined Python functions and external services.

```python
from bindai import Agent


def get_status() -> str:
    return "All systems operational."


agent = (
    Agent.builder()
    .name("assistant")
    .instructions("You are a helpful assistant.")
    .model("openai:gpt-4.1-mini")
    .tool(get_status)
    .build()
)
```

Tools can be combined with workflows, Memory, Knowledge, Connections, and multi-agent systems.

---

## Workflows

BindAI provides workflow orchestration capabilities for composing AI and application operations.

Supported workflow patterns include:

* Sequential execution
* Conditional branching
* Loops
* Parallel execution
* Retries
* Timeouts
* Human-in-the-loop tasks
* Scheduling
* External integrations

Workflows can coordinate agents, tools, retrieval, memory, and external services.

---

## Memory

Memory provides provider-based storage and retrieval of application records.

Current memory providers include:

* In-memory
* SQLite
* PostgreSQL
* Vector memory
* Pinecone
* Chroma

Memory can store application state, long-term information, metadata, relationships, embeddings, and other records.

Example:

```python
from bindai import Agent
from bindai_memory import Memory, SQLiteMemoryProvider


memory = Memory(
    SQLiteMemoryProvider("memory.db")
)

agent = (
    Agent.builder()
    .name("assistant")
    .instructions("You are a helpful assistant.")
    .model("openai:gpt-4.1-mini")
    .memory(memory)
    .build()
)
```

---

## Knowledge and RAG

BindAI includes a Knowledge layer for retrieval-augmented applications.

The Knowledge and retrieval stack supports:

* Document loading
* Ingestion
* Parsing
* Chunking
* Metadata
* Embeddings
* Vector retrieval
* BM25 retrieval
* Hybrid retrieval
* Metadata filtering
* Reranking
* Conversational retrieval
* Knowledge pipelines
* Agent integration

The framework also provides an OpenAI embedding provider and a deterministic local embedding provider for development and testing.

---

## Embeddings and Retrieval

Embeddings and retrieval are available as modular packages.

Retrieval capabilities include:

* Vector search
* BM25 search
* Hybrid search
* Similarity scoring
* Metadata filtering
* Search configuration
* Reranking

These components can be used independently or combined with the Knowledge and agent layers.

---

## Multi-Agent Systems

Agents can delegate work to other agents and participate in agent teams.

Current capabilities include:

* Agent delegation
* Team delegation
* Specialist agents
* Role-based chains
* Retrieval-enabled agents

More advanced planning and hierarchical coordination remain part of the roadmap.

---

## External Connections

The Connections package provides a common abstraction for integrating external services.

Current integrations include:

* Webhooks
* GitHub
* Slack
* Notion
* Jira
* Discord
* Resend
* Vercel
* Netlify

Connections are modular and can be used by application logic, tools, workflows, and agents.

---

## MCP

BindAI includes a basic MCP client integration for connecting applications to MCP-compatible tool services.

Current MCP capabilities include:

* Tool discovery
* Tool calling
* Basic HTTP connections

Additional MCP capabilities are planned as the integration evolves.

---

# AI Providers

BindAI currently includes provider integrations for:

* OpenAI
* Anthropic
* Google Gemini
* Groq
* Ollama
* OpenRouter

Providers are packaged independently so applications can select the provider they need.

Typical model identifiers use:

```text
provider:model
```

Examples:

```text
openai:gpt-4.1-mini
anthropic:claude-sonnet-4
google:gemini-2.5-flash
groq:llama-3.3-70b-versatile
ollama:llama3
openrouter:openai/gpt-4.1-mini
```

Provider packages are separate from the main `bindai` package.

---

# Package Ecosystem

BindAI is organized as a modular package ecosystem.

| Package                 | Purpose                      |
| ----------------------- | ---------------------------- |
| `bindai`                | Main framework               |
| `bindai-agent`          | AI agents                    |
| `bindai-application`    | Application abstractions     |
| `bindai-cli`            | Command-line interface       |
| `bindai-config`         | Configuration                |
| `bindai-connections`    | External service connections |
| `bindai-core`           | Core framework primitives    |
| `bindai-embeddings`     | Embedding providers          |
| `bindai-group`          | Agent groups                 |
| `bindai-host`           | Hosting-related components   |
| `bindai-knowledge`      | Knowledge and RAG            |
| `bindai-mcp`            | MCP integration              |
| `bindai-memory`         | Memory providers             |
| `bindai-model`          | Model abstractions           |
| `bindai-project`        | Project abstractions         |
| `bindai-prompt-builder` | Prompt construction          |
| `bindai-prompts`        | Prompt system                |
| `bindai-providers`      | Provider infrastructure      |
| `bindai-retrieval`      | Retrieval                    |
| `bindai-runtime`        | Runtime                      |
| `bindai-task`           | Tasks                        |
| `bindai-tool`           | Tool system                  |
| `bindai-workflow`       | Workflow orchestration       |

Provider integrations are packaged separately under the provider namespace:

```text
bindai-provider-openai
bindai-provider-anthropic
bindai-provider-google
bindai-provider-groq
bindai-provider-ollama
bindai-provider-openrouter
```

---

# Architecture

```text
                    Application
                         |
             +-----------+-----------+
             |           |           |
           Agent      Workflow     Tools
             |           |           |
             +-----------+-----------+
                         |
              +----------+----------+
              |                     |
            Memory              Knowledge
                                    |
                              Retrieval / RAG
                                    |
                         +----------+----------+
                         |                     |
                    Embeddings             Reranking
                         |
                  Model Providers
                         |
       +---------+---------+---------+---------+
       |         |         |         |         |
     OpenAI   Anthropic  Google    Groq     Ollama
                                               |
                                         OpenRouter
```

External Connections and MCP can be integrated alongside these application components.

The architecture is designed around composable packages so individual capabilities can evolve independently.

---

# Project Structure

```text
BindAI/

â”œâ”€â”€ packages/
â”‚   â”œâ”€â”€ bindai/
â”‚   â”œâ”€â”€ bindai-agent/
â”‚   â”œâ”€â”€ bindai-core/
â”‚   â”œâ”€â”€ bindai-memory/
â”‚   â”œâ”€â”€ bindai-tool/
â”‚   â”œâ”€â”€ bindai-workflow/
â”‚   â”œâ”€â”€ bindai-knowledge/
â”‚   â”œâ”€â”€ bindai-connections/
â”‚   â”œâ”€â”€ bindai-mcp/
â”‚   â””â”€â”€ ...

â”œâ”€â”€ docs/
â”œâ”€â”€ scripts/

â”œâ”€â”€ README.md
â”œâ”€â”€ docs.json
â””â”€â”€ pyproject.toml
```

---

# Documentation

Complete documentation is available at:

**https://docs.bindai.dev**

Documentation includes:

* Getting Started
* Installation
* Core Concepts
* Agents
* Tools
* Memory
* Knowledge and RAG
* Workflows
* Projects
* Connections
* MCP
* API Reference

---

# Roadmap

BindAI is being developed incrementally.

Current roadmap areas include:

* AI application foundation
* AI provider ecosystem
* Memory, storage, and retrieval
* Advanced Knowledge and RAG
* Connections and integrations
* MCP
* Advanced agents and multi-agent systems
* AI automation
* Public API and deployment
* Observability

Future areas include:

* Enterprise capabilities
* Visual workflow platform
* Voice AI
* Templates and business solutions

See the current roadmap in the documentation for implementation status and upcoming work.

---

# Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add or update tests when appropriate.
5. Verify the test suite.
6. Submit a pull request.

Bug reports, documentation improvements, feature requests, and code contributions are welcome.

---

# Community

* Documentation: https://docs.bindai.dev
* Website: https://bindai.dev
* GitHub: https://github.com/BindBrain/BindAI

Follow BindAI and BindBrain for project updates and future ecosystem announcements.

---

# License

BindAI is released under the **MIT License**.

---

# Vision

BindAI aims to provide an open-source foundation for building AI software with composable, provider-independent components.

The long-term vision is to support increasingly sophisticated AI applications while keeping the underlying architecture modular, testable, and extensible.

---

<p align="center">

<strong>Build AI Software. Scale Everywhere.</strong>

Made with â¤ï¸ by <strong>BindBrain</strong>

https://bindai.dev

</p>
