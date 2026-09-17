# BindAI

Build production-ready AI applications with a modern Python framework for AI agents, workflows, tools, memory, knowledge, and retrieval.

BindAI provides a composable Python API for building AI applications while keeping providers, workflows, memory, tools, and project configuration modular.

## Installation

Install the core framework from PyPI:

```bash
pip install bindai
```

Provider implementations are installed through optional extras:

```bash
pip install "bindai[openai]"
```

Available provider extras:

- `openai`
- `anthropic`
- `google`
- `groq`
- `ollama`
- `openrouter`

For example:

```bash
pip install "bindai[anthropic]"
```

BindAI requires Python 3.12 or newer.

## Quick Start

Configure your provider credentials through the environment:

```bash
export OPENAI_API_KEY="your-api-key"
```

Then create an agent:

```python
from bindai import Agent

agent = (
    Agent.builder()
    .openai("gpt-4.1-mini")
    .instructions("You are a helpful assistant.")
    .build()
)

result = agent.run("Hello!")

print(result.output)
```

The same agent API can be configured through project configuration and provider connections.

## Core Capabilities

### AI Agents

Build agents with configurable providers, models, instructions, tools, memory, and execution behavior.

```python
from bindai import Agent

agent = (
    Agent.builder()
    .openai("gpt-4.1-mini")
    .instructions("You are a helpful assistant.")
    .build()
)
```

### Workflows

Compose multi-step AI processes using workflow nodes, conditions, loops, parallel execution, retries, timeouts, scheduling, and human tasks.

```python
from bindai import Workflow

workflow = Workflow.builder() \
    .name("research-workflow") \
    .build()
```

### Tools

Extend agents with Python functions and reusable tools.

```python
from bindai import tool

@tool
def get_weather(city: str) -> str:
    return f"Weather information for {city}"
```

### Memory

Store and retrieve conversational or application state through BindAI memory providers.

Supported memory capabilities include:

- In-memory storage
- SQLite-backed storage
- PostgreSQL-backed storage
- Vector memory
- Custom memory providers

### Knowledge and Retrieval

Build retrieval-augmented applications from documents, embeddings, and retrievers.

BindAI provides building blocks for:

- Document ingestion
- Embeddings
- Retrievers
- Retrieval pipelines
- RAG applications

### Multi-Agent Systems

Compose multiple agents and tasks for applications that require specialized roles or coordinated execution.

## Provider Connections

BindAI supports project-scoped provider connections so API credentials do not need to be stored directly in project configuration.

A connection consists of provider metadata in the project manifest and a credential stored through the operating system credential store.

Create a connection with the CLI:

```bash
bindai connections add work --provider openai
```

List configured connections:

```bash
bindai connections list
```

Remove a connection:

```bash
bindai connections remove work
```

The project manifest is stored at:

```text
.bindai/connections.toml
```

The credential itself is stored through the operating system credential store rather than in the project manifest.

Select the connection in `bindai.toml`:

```toml
provider = "openai"
connection = "work"
model = "gpt-4.1-mini"
```

Agents created through the project configuration can then resolve the configured provider connection.

For example:

```python
from bindai import Agent

agent = Agent.builder().build()
result = agent.run("Hello!")

print(result.output)
```

Provider credential resolution follows this precedence:

1. Explicit API key supplied to the builder
2. Credential from the configured project connection
3. Provider environment variable

For example, an OpenAI provider normally uses:

```text
OPENAI_API_KEY
OPENAI_BASE_URL
OPENAI_ORGANIZATION
```

Validate project configuration and connection state with:

```bash
bindai doctor
```

## External Connections

BindAI also provides connection capabilities for external application services. These are separate from model-provider connections.

Supported integrations include:

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

These integrations can be used by applications and tools to interact with external services.

## MCP

BindAI includes Model Context Protocol (MCP) support for connecting agents and applications to MCP-based tools and services.

MCP capabilities include:

- MCP client support
- Tool discovery
- Tool invocation
- Basic HTTP-based MCP connectivity

## AI Providers

BindAI supports multiple model providers through separate provider packages.

### OpenAI

```bash
pip install "bindai[openai]"
```

```python
from bindai import Agent

agent = (
    Agent.builder()
    .openai("gpt-4.1-mini")
    .instructions("You are a helpful assistant.")
    .build()
)
```

### Anthropic

```bash
pip install "bindai[anthropic]"
```

### Google Gemini

```bash
pip install "bindai[google]"
```

### Groq

```bash
pip install "bindai[groq]"
```

### Ollama

```bash
pip install "bindai[ollama]"
```

### OpenRouter

```bash
pip install "bindai[openrouter]"
```

Provider implementations are distributed independently from the shared provider registry and configuration layer.

## Package Ecosystem

BindAI is organized as a collection of focused packages.

| Package | Purpose |
| --- | --- |
| `bindai` | Main framework distribution |
| `bindai-core` | Core abstractions and shared types |
| `bindai-agent` | Agent construction and execution |
| `bindai-application` | Application-level functionality |
| `bindai-config` | Project configuration and resolution |
| `bindai-connections` | Connection abstractions and credential storage |
| `bindai-group` | Multi-agent groups |
| `bindai-knowledge` | Knowledge and document capabilities |
| `bindai-memory` | Memory abstractions and providers |
| `bindai-model` | Model abstractions |
| `bindai-project` | Project runtime and project configuration |
| `bindai-retrieval` | Retrieval functionality |
| `bindai-runtime` | Runtime support |
| `bindai-task` | Task abstractions |
| `bindai-workflow` | Workflow construction and execution |
| `bindai-providers` | Provider registry and shared provider infrastructure |
| `bindai-provider-openai` | OpenAI provider implementation |
| `bindai-provider-anthropic` | Anthropic provider implementation |
| `bindai-provider-google` | Google provider implementation |
| `bindai-provider-groq` | Groq provider implementation |
| `bindai-provider-ollama` | Ollama provider implementation |
| `bindai-provider-openrouter` | OpenRouter provider implementation |
| `bindai-cli` | BindAI command-line interface |

The `bindai` distribution installs the core framework packages. Provider implementations are available through the corresponding optional extras.

## Architecture

BindAI separates application concerns into focused layers:

```text
Application
    │
    ├── Agents
    ├── Workflows
    ├── Tasks
    ├── Tools
    ├── Memory
    └── Knowledge
          │
          ▼
       Runtime
          │
          ▼
      Model Layer
          │
          ▼
   Provider Registry
          │
          ├── OpenAI
          ├── Anthropic
          ├── Google
          ├── Groq
          ├── Ollama
          └── OpenRouter
```

This structure allows individual components to evolve independently while providing a unified framework API.

## Project Structure

A BindAI project can contain application configuration, agents, workflows, tools, memory, knowledge, and templates:

```text
my-project/
├── bindai.toml
├── .bindai/
│   └── connections.toml
├── agents/
├── workflows/
├── tools/
├── memory/
├── knowledge/
└── templates/
```

Project configuration can define the default provider, model, connection, and runtime settings.

Example:

```toml
name = "My BindAI Project"
provider = "openai"
connection = "work"
model = "gpt-4.1-mini"
temperature = 0.7
timeout = 60
```

## Documentation

Full documentation is available at:

https://docs.bindai.dev

The documentation covers:

- Getting started
- Agents
- Prompts
- Execution
- Providers
- Results
- Events
- Tools
- MCP
- Memory
- Knowledge and RAG
- Workflows
- Projects
- Templates
- Connections
- API reference
- Automation

## Roadmap

BindAI is evolving toward a complete framework for production AI applications.

Current development areas include:

- Agent and workflow reliability
- Provider integrations
- Project configuration
- Secure provider connections
- Memory and knowledge systems
- MCP integrations
- Automation
- Service APIs
- Deployment and observability

See the repository roadmap for the current project status and planned work.

## Examples

Example applications and workflow templates are maintained in the BindAI repository.

Repository:

https://github.com/BindBrain/BindAI

## Contributing

Contributions are welcome.

Before submitting changes:

1. Create a focused branch.
2. Make the smallest appropriate change.
3. Add or update tests when behavior changes.
4. Run the relevant test suite.
5. Run the project linting and validation checks.
6. Open a pull request with a clear description of the change.

## Community

Issues, feature requests, and discussions are managed through the BindAI GitHub repository.

https://github.com/BindBrain/BindAI

## License

BindAI is released under the project's open-source license.

See the repository `LICENSE` file for the complete license text.

## Vision

BindAI aims to provide a practical foundation for building AI applications that combine agents, tools, workflows, memory, knowledge, model providers, and external services in a single composable Python framework.