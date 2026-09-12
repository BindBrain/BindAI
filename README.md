# BindAI

Build AI software, not just AI demos.

BindAI is a modular Python framework for building AI applications with reusable components for agents, tools, workflows, memory, knowledge and RAG, model providers, integrations, automation, and more.

Whether you're building an AI assistant, document-processing application, workflow automation, or multi-agent system, BindAI provides building blocks that can grow with your application.

## Installation

### Install from PyPI

```bash
python -m pip install bindai
```

Verify the installation:

```bash
bindai version
```

> Note: use `bindai version` to display the installed CLI version.

### Install from GitHub for development

Clone the repository:

```bash
git clone https://github.com/BindBrain/BindAI.git

cd BindAI
```

BindAI is organized as a multi-package **uv workspace**.

Install the development workspace with:

```bash
python -m pip install uv

uv sync
```

Activate the environment.

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

Verify the development installation:

```bash
python -c "import bindai; print('BindAI import OK')"

bindai version
```

The repository root is a workspace containing multiple BindAI packages. Do not use `pip install -e .` from the repository root.

Individual packages are located under:

```text
packages/
```

and are managed together through the workspace configuration.

## Quick Start

The recommended agent construction API is `Agent.builder()`:

```python
from bindai import Agent

agent = Agent.builder().name("assistant").instructions("You are a helpful AI assistant.").build()

response = agent.run("Explain what BindAI is.")

print(response.output)
```

You can incrementally add capabilities such as:

* Tools
* Memory
* Knowledge and RAG
* Workflows
* Human approval
* Scheduling
* Multiple AI providers
* Multi-agent execution
* Automation
* External integrations
* MCP tools

## Core Capabilities

### Agents

BindAI agents provide the foundation for AI application execution.

Current capabilities include:

* Agent construction and configuration
* Conversation management
* Prompt management
* Tool calling
* Structured outputs
* Streaming responses
* Memory integration
* Knowledge and retrieval integration
* Agent delegation
* Multi-agent team execution

### Tools

Tools allow agents and workflows to interact with application functionality and external systems.

Current capabilities include:

* Automatic tool registration
* Function schema generation
* Tool metadata
* Context-aware execution
* Tool results
* MCP-discovered tools
* Advanced tool execution

### Workflows

BindAI workflows provide orchestration around agents and other workflow nodes.

Supported workflow patterns include:

* Sequential execution
* Conditional branching
* Loops
* Parallel execution
* Retry policies
* Timeouts
* Human tasks
* Scheduling

### Memory

BindAI provides pluggable memory infrastructure for conversation and long-term application context.

Current memory implementations include:

* In-memory memory
* SQLite
* PostgreSQL
* Vector memory
* Pinecone
* Chroma

### Knowledge and RAG

BindAI provides a Knowledge and Retrieval architecture for document-based AI applications.

Current capabilities include:

* Document loading
* Document chunking
* Embeddings
* Vector retrieval
* BM25 retrieval
* Hybrid retrieval
* Reranking
* Conversational retrieval
* Knowledge ingestion pipelines
* RAG integration

### AI Providers

BindAI currently supports:

* OpenAI
* Anthropic
* Google Gemini
* Groq
* Ollama
* OpenRouter

The provider architecture is modular so additional providers can be added independently.

### Connections

BindAI provides a connection layer for external services.

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

### MCP

BindAI includes MCP client support for discovering and calling tools exposed through an MCP-compatible HTTP service.

### Automation

BindAI provides an automation layer for defining, executing, tracking, and running automations in the background.

Current automation capabilities include:

* Automation definitions
* Event trigger framework
* Unified trigger management
* Automation execution runs
* Persistent automation state abstractions
* Automation run history
* In-memory state storage
* In-memory run history
* Background automation workers

Automation execution is built on top of BindAI's existing executable and runtime architecture rather than introducing a separate execution model.

## Package Ecosystem

BindAI is built as a modular package ecosystem.

| Package                 | Purpose                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| `bindai`                | Main framework package                                                  |
| `bindai-agent`          | AI agent framework                                                      |
| `bindai-application`    | Application layer                                                       |
| `bindai-automation`     | Automation definitions, triggers, execution state, history, and workers |
| `bindai-cli`            | Command-line interface                                                  |
| `bindai-config`         | Configuration                                                           |
| `bindai-connections`    | External connections and integrations                                   |
| `bindai-core`           | Core framework abstractions                                             |
| `bindai-embeddings`     | Embedding providers                                                     |
| `bindai-group`          | Agent groups and multi-agent execution                                  |
| `bindai-host`           | Hosting infrastructure                                                  |
| `bindai-knowledge`      | Knowledge and RAG                                                       |
| `bindai-mcp`            | MCP client support                                                      |
| `bindai-memory`         | Memory providers                                                        |
| `bindai-model`          | Model abstractions                                                      |
| `bindai-project`        | Project management                                                      |
| `bindai-prompt-builder` | Prompt construction                                                     |
| `bindai-prompts`        | Prompt system                                                           |
| `bindai-providers`      | Provider abstractions and registry                                      |
| `bindai-retrieval`      | Retrieval implementations                                               |
| `bindai-runtime`        | Runtime infrastructure                                                  |
| `bindai-task`           | Tasks and human tasks                                                   |
| `bindai-tool`           | Tool system                                                             |
| `bindai-workflow`       | Workflow engine                                                         |

Provider implementations are distributed as separate packages, including:

* `bindai-provider-openai`
* `bindai-provider-anthropic`
* `bindai-provider-google`
* `bindai-provider-groq`
* `bindai-provider-ollama`
* `bindai-provider-openrouter`

Each package can evolve independently while remaining part of the BindAI ecosystem.

## Architecture

```text
                         AI Application
                               |
          +--------------------+--------------------+
          |                    |                    |
        Agents             Workflows             Tools
          |                    |                    |
          +--------------------+--------------------+
                               |
                 +-------------+-------------+
                 |                           |
              Memory                    Knowledge
                 |                           |
                 +-------------+-------------+
                               |
                        Retrieval / RAG
                               |
          +--------------------+--------------------+
          |                    |                    |
      Providers          Connections               MCP
          |                    |                    |
          +--------------------+--------------------+
                               |
                         Automation
                               |
             +-----------------+-----------------+
             |                 |                 |
          Triggers           Runs             Workers
             |                 |                 |
             +-----------------+-----------------+
                               |
                     Execution Infrastructure
                               |
                       Runtime / Core
```

The architecture is intentionally modular. Applications can use individual components or combine them into larger AI systems.

Automation builds on the same executable and runtime abstractions used by the rest of BindAI, while keeping automation state and historical run records in the automation layer.

## Project Structure

```text
BindAI/
|
+-- packages/
|   +-- bindai/
|   +-- bindai-agent/
|   +-- bindai-application/
|   +-- bindai-automation/
|   +-- bindai-core/
|   +-- bindai-memory/
|   +-- bindai-knowledge/
|   +-- bindai-retrieval/
|   +-- bindai-tool/
|   +-- bindai-workflow/
|   +-- bindai-connections/
|   +-- bindai-mcp/
|   +-- providers/
|       +-- bindai-provider-openai/
|       +-- bindai-provider-anthropic/
|       +-- bindai-provider-google/
|       +-- bindai-provider-groq/
|       +-- bindai-provider-ollama/
|       +-- bindai-provider-openrouter/
|
+-- docs/
+-- examples/
+-- scripts/
|
+-- CHANGELOG.md
+-- CONTRIBUTING.md
+-- CODE_OF_CONDUCT.md
+-- SECURITY.md
+-- LICENSE
+-- README.md
+-- RELEASE.md
+-- docs.json
+-- pyproject.toml
```

## Documentation

Full documentation is available at:

https://docs.bindai.dev

The documentation currently covers:

* Getting Started
* Core Concepts
* Agents
* Tools
* Memory
* Knowledge and RAG
* Workflows
* Projects
* Connections
* Automation
* API Reference
* Roadmap

The `examples/` directory also contains runnable examples covering many current BindAI capabilities.

## Roadmap

BindAI is being developed incrementally across several areas.

Current and planned areas include:

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
* Enterprise capabilities
* Visual workflow tooling
* Voice AI
* Templates and business solutions

See the current roadmap in the documentation for implementation status and priorities.

## Examples

The repository contains examples demonstrating current framework capabilities.

```text
examples/
```

Examples cover areas such as:

* Basic agents
* Tools
* Streaming
* Memory
* Knowledge and RAG
* Workflows
* Multi-agent execution
* Human approval
* Retry and timeout handling
* FastAPI integration
* CLI usage
* MCP
* Custom providers
* Custom embeddings
* Custom memory
* Custom retrievers
* Configuration
* Automation
* Production-oriented application structure

The examples are intended to demonstrate framework usage and should be evaluated according to the maturity of the underlying APIs.

## Contributing

Contributions are welcome.

Before contributing, please read:

* `CONTRIBUTING.md`
* `CODE_OF_CONDUCT.md`
* `SECURITY.md`

Typical development setup:

```bash
uv sync
```

Run the test suite with:

```bash
uv run pytest
```

Run linting with:

```bash
uv run ruff check .
```

Check formatting with:

```bash
uv run ruff format --check .
```

Please add or update tests when changing framework behavior.

## Community

* Documentation: https://docs.bindai.dev
* GitHub: https://github.com/BindBrain/BindAI
* Website: https://bindai.dev

## License

BindAI is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

## Vision

BindAI aims to become a complete open-source ecosystem for building AI software.

The long-term vision includes:

* Production-oriented AI applications
* Modular AI infrastructure
* Advanced agent and multi-agent systems
* AI workflow automation
* Enterprise integrations
* Visual workflow tooling
* Developer-focused AI application infrastructure

## Status

BindAI is under active development.

The framework already provides a substantial foundation for agents, workflows, tools, memory, knowledge and RAG, providers, integrations, MCP, multi-agent execution, and automation.

Current automation capabilities include automation definitions, event triggers, execution state, run history, and background workers.

Some roadmap areas remain under development and should not yet be considered complete production platform capabilities.

**Build AI Software. Scale Everywhere.**

Made with ♥ by **BindBrain**