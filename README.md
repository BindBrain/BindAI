# BindAI

Build AI software.

BindAI is an open-source, modular Python framework for building AI applications with reusable components for agents, tools, workflows, memory, knowledge and RAG, model providers, integrations, automation, and runtime infrastructure.

Whether you're building an AI assistant, document-processing application, workflow automation, or multi-agent system, BindAI provides building blocks that can grow with your application.

## v0.1

BindAI v0.1 establishes the first public release foundation for building and deploying AI applications.

The v0.1 release includes:

- AI agents and agent execution
- Tools and tool calling
- Workflows and workflow orchestration
- Memory
- Knowledge and RAG
- Multiple model providers
- Multi-agent execution
- External service connections
- MCP HTTP tool integration
- Automation definitions and event triggers
- Background automation workers
- REST Service API
- API authentication
- Project, agent, workflow, and run execution APIs
- Streaming API responses
- Docker and Docker Compose deployment
- Runtime execution events and observability foundation

Some advanced distributed infrastructure and enterprise capabilities remain post-v0.1 roadmap work.

## Installation

### Install from PyPI

Install the main BindAI package:

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

agent = (
    Agent.builder()
    .name("assistant")
    .instructions("You are a helpful AI assistant.")
    .build()
)

response = agent.run("Explain what BindAI is.")

print(response.output)
```

You can incrementally add capabilities such as:

- Tools
- Memory
- Knowledge and RAG
- Workflows
- Human approval
- Scheduling
- Multiple AI providers
- Multi-agent execution
- Automation
- External integrations
- MCP tools

## Core Capabilities

### Agents

BindAI agents provide the foundation for AI application execution.

Current capabilities include:

- Agent construction and configuration
- Conversation management
- Prompt management
- Tool calling
- Structured outputs
- Streaming responses
- Memory integration
- Knowledge and retrieval integration
- Agent delegation
- Multi-agent team execution

### Tools

Tools allow agents and workflows to interact with application functionality and external systems.

Current capabilities include:

- Automatic tool registration
- Function schema generation
- Tool metadata
- Context-aware execution
- Tool results
- MCP-discovered tools
- Tool execution through the runtime

### Workflows

BindAI workflows provide orchestration around agents and other workflow nodes.

Supported workflow patterns include:

- Sequential execution
- Conditional branching
- Loops
- Parallel execution
- Retry policies
- Timeouts
- Human tasks
- Scheduling

### Memory

BindAI provides pluggable memory infrastructure for conversation and long-term application context.

Current memory implementations include:

- In-memory memory
- SQLite
- PostgreSQL
- Vector memory
- Pinecone
- Chroma

### Knowledge and RAG

BindAI provides a Knowledge and Retrieval architecture for document-based AI applications.

Current capabilities include:

- Document loading
- Document chunking
- Embeddings
- Vector retrieval
- BM25 retrieval
- Hybrid retrieval
- Reranking
- Conversational retrieval
- Knowledge ingestion pipelines
- RAG integration

### AI Providers

BindAI supports a modular provider architecture for connecting AI applications to different model providers.

Current providers include:

- OpenAI
- Anthropic
- Google Gemini
- Groq
- Ollama
- OpenRouter

The provider architecture is modular so additional providers can be added independently.

### Connections

BindAI provides a connection layer for external services.

Current v0.1 integrations include:

- Webhooks
- GitHub
- Slack
- Notion
- Jira
- Discord
- Resend
- Vercel
- Netlify
- Google Sheets
- Google Docs
- Gmail
- Google Drive

Connections can be used as reusable integration components for applications, agents, workflows, and automation.

### MCP

BindAI v0.1 includes a lightweight MCP HTTP integration for discovering and calling tools exposed through an MCP-compatible HTTP service.

The MCP package provides:

- MCP tool discovery
- Remote tool definitions
- Tool schema propagation
- HTTP-based tool execution
- Integration with BindAI's tool system

The current implementation is intentionally lightweight. It is an HTTP bridge for MCP-style tool discovery and execution rather than a complete MCP server or full MCP protocol implementation.

### Automation

BindAI provides an automation layer for defining, executing, tracking, and running automations in the background.

Current automation capabilities include:

- Automation definitions
- Event trigger framework
- Unified trigger management
- Automation execution runs
- Persistent automation state abstractions
- Automation run history
- In-memory state storage
- In-memory run history
- Background automation workers

The current background worker uses a process-local thread pool. Distributed queues and horizontally scalable worker infrastructure are planned for later releases.

Automation execution is built on top of BindAI's existing executable and runtime architecture rather than introducing a separate execution model.

### Service API

BindAI v0.1 includes a REST API package for exposing BindAI applications and execution capabilities as a service.

The API currently provides:

- Health checks
- API key authentication
- Agent execution
- Workflow execution
- Project execution
- Run tracking
- Streaming responses
- Background execution

The API uses FastAPI and can be run with Uvicorn.

Example:

```bash
uv run uvicorn bindai_api.app:app --host 0.0.0.0 --port 8000
```

The health endpoint is publicly accessible:

```text
GET /health
```

Protected API routes use:

```text
Authorization: Bearer <BINDAI_API_KEY>
```

The Service API is intended to provide the foundation for deploying BindAI applications as services.

### Deployment

BindAI v0.1 includes Docker and Docker Compose support for running the Service API and its supporting runtime.

Build the Docker image:

```bash
docker build -t bindai .
```

Run the API container:

```bash
docker run --rm -p 8000:8000 bindai
```

The repository also includes Docker Compose configuration for local multi-service development and deployment.

The v0.1 deployment model is intentionally straightforward. Distributed queues, Kubernetes deployment, and horizontally scalable worker infrastructure are planned for later releases.

### Observability

BindAI v0.1 includes an event-driven observability foundation across runtime and agent execution.

Current capabilities include:

- Runtime execution events
- Event bus infrastructure
- Execution context
- Agent lifecycle events
- Model request and response events
- Tool execution events
- In-memory event recording
- Event retrieval by execution

The current observability layer provides the foundation for future tracing, metrics, dashboards, and external observability integrations.

It should not yet be considered a complete production monitoring platform.

## Package Ecosystem

BindAI is built as a modular package ecosystem.

| Package | Purpose |
| --- | --- |
| `bindai` | Main framework package |
| `bindai-agent` | AI agent framework |
| `bindai-application` | Application layer |
| `bindai-automation` | Automation definitions, triggers, execution state, history, and workers |
| `bindai-cli` | Command-line interface |
| `bindai-config` | Configuration |
| `bindai-connections` | External connections and integrations |
| `bindai-core` | Core framework abstractions |
| `bindai-embeddings` | Embedding providers |
| `bindai-group` | Agent groups and multi-agent execution |
| `bindai-host` | Hosting infrastructure |
| `bindai-knowledge` | Knowledge and RAG |
| `bindai-mcp` | MCP HTTP tool integration |
| `bindai-memory` | Memory providers |
| `bindai-model` | Model abstractions |
| `bindai-project` | Project management |
| `bindai-prompt-builder` | Prompt construction |
| `bindai-prompts` | Prompt system |
| `bindai-providers` | Provider abstractions and registry |
| `bindai-retrieval` | Retrieval implementations |
| `bindai-runtime` | Runtime infrastructure and execution events |
| `bindai-task` | Tasks and human tasks |
| `bindai-tool` | Tool system |
| `bindai-workflow` | Workflow engine |

The repository is structured as a workspace so individual packages can evolve independently while remaining part of the BindAI ecosystem.

## Architecture

```text
                         AI Application
                               |
              +----------------+----------------+
              |                |                |
            Agents          Workflows         Tools
              |                |                |
              +----------------+----------------+
                               |
                 +-------------+-------------+
                 |                           |
              Memory                    Knowledge
                 |                           |
                 +-------------+-------------+
                               |
                         Retrieval / RAG
                               |
              +----------------+----------------+
              |                |                |
          Providers       Connections          MCP
              |                |                |
              +----------------+----------------+
                               |
                          Automation
                               |
                 +-------------+-------------+
                 |             |             |
              Triggers       Runs         Workers
                 |             |             |
                 +-------------+-------------+
                               |
                    Service API / Deployment
                               |
                    Runtime / Core
                               |
                         Observability
```

The architecture is intentionally modular. Applications can use individual components or combine them into larger AI systems.

Automation builds on the same executable and runtime abstractions used by the rest of BindAI, while keeping automation state and historical run records in the automation layer.

The Service API provides an application-facing HTTP layer over the underlying framework and runtime.

## Project Structure

```text
BindAI/
|
+-- packages/
|   +-- bindai/
|   +-- bindai-agent/
|   +-- bindai-application/
|   +-- bindai-automation/
|   +-- bindai-cli/
|   +-- bindai-config/
|   +-- bindai-connections/
|   +-- bindai-core/
|   +-- bindai-embeddings/
|   +-- bindai-group/
|   +-- bindai-host/
|   +-- bindai-knowledge/
|   +-- bindai-mcp/
|   +-- bindai-memory/
|   +-- bindai-model/
|   +-- bindai-project/
|   +-- bindai-prompt-builder/
|   +-- bindai-prompts/
|   +-- bindai-providers/
|   +-- bindai-retrieval/
|   +-- bindai-runtime/
|   +-- bindai-task/
|   +-- bindai-tool/
|   +-- bindai-workflow/
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
+-- Dockerfile
+-- docker-compose.yml
+-- pyproject.toml
```

## Documentation

Full documentation is available at:

https://docs.bindai.dev

The documentation currently covers:

- Getting Started
- Core Concepts
- Agents
- Tools
- Memory
- Knowledge and RAG
- Workflows
- Projects
- Connections
- Automation
- Service API
- API Authentication
- Streaming
- Background Runs
- Deployment
- MCP
- Roadmap

The `examples/` directory also contains runnable examples covering many current BindAI capabilities.

## Roadmap

BindAI is being developed incrementally.

### v0.1 release foundation

The v0.1 release establishes the foundation for:

- AI agents
- Workflows
- Tools
- Memory
- Knowledge and RAG
- Model providers
- Multi-agent execution
- External connections
- MCP HTTP integration
- Automation
- Background workers
- REST Service API
- Docker and Compose deployment
- Runtime observability foundation

### Post-v0.1 development

Future development areas include:

- Distributed queues
- Horizontally scalable workers
- Kubernetes deployment
- Advanced tracing and metrics
- Advanced agent capabilities
- Expanded automation infrastructure
- Additional integrations
- Visual workflow tooling
- Enterprise capabilities
- Voice AI
- Templates and business solutions

See the current roadmap in the documentation for implementation status and priorities.

## Examples

The repository contains examples demonstrating current framework capabilities.

```text
examples/
```

Examples cover areas such as:

- Basic agents
- Tools
- Streaming
- Memory
- Knowledge and RAG
- Workflows
- Multi-agent execution
- Human approval
- Retry and timeout handling
- FastAPI integration
- CLI usage
- MCP
- Custom providers
- Custom embeddings
- Custom memory
- Custom retrievers
- Configuration
- Automation
- Production-oriented application structure

The examples are intended to demonstrate framework usage and should be evaluated according to the maturity of the underlying APIs.

## Contributing

Contributions are welcome.

Before contributing, please read:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`

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

Run type checking with:

```bash
uv run mypy packages examples
```

Please add or update tests when changing framework behavior.

## Community

- Documentation: https://docs.bindai.dev
- GitHub: https://github.com/BindBrain/BindAI
- Website: https://bindai.dev

## License

BindAI is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

## Vision

BindAI aims to become a complete open-source ecosystem for building AI software.

The long-term vision includes:

- Production-oriented AI applications
- Modular AI infrastructure
- Advanced agent and multi-agent systems
- AI workflow automation
- Enterprise integrations
- Visual workflow tooling
- Developer-focused AI application infrastructure

## Status

BindAI is under active development.

**BindAI v0.1 establishes the first public release foundation** for building, integrating, automating, and deploying AI applications.

The current release provides a substantial foundation for:

- Agents
- Workflows
- Tools
- Memory
- Knowledge and RAG
- Model providers
- Multi-agent execution
- External connections
- MCP tool integration
- Automation
- Background workers
- REST APIs
- Docker deployment
- Runtime observability

The v0.1 automation system includes automation definitions, event triggers, execution state, run history, and background workers.

The v0.1 Service API provides authenticated REST endpoints for application execution, projects, workflows, agents, runs, streaming, and background execution.

Some roadmap areas remain under development and should not yet be considered complete distributed or enterprise platform capabilities.

**Build AI Software. Scale Everywhere.**

Made with ♥ by **BindBrain**