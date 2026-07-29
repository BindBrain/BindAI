BindAI

Build AI applications with agents, tools...

Features

Installation

Quick Start

Examples
...

# BindAI

> A modern Python framework for building agentic AI applications.

BindAI is an open-source framework that provides the building blocks required to create AI agents, workflows, tools, providers, memory systems, and execution pipelines.

The goal of BindAI is to provide a clean, modular, provider-agnostic architecture for building production-ready AI systems.

---

## Features

Current features included in **v0.1.0**

- Multi-provider architecture
- Agent framework
- Tool calling
- Conversation management
- Prompt templates
- Middleware pipeline
- Dependency Injection
- Execution pipeline
- Streaming responses
- Extensible provider system
- Provider registry and factory
- Tool schema generation
- Automatic tool registration

---

## Installation

Clone the repository:

```bash
git clone https://github.com/BindBrain/BindAI.git

cd bindai
```

Install the core package in editable mode:

```bash
pip install -e packages/bindai-core
```

---

## Quick Start

```python
from bindai_core import AssistantAgent

agent = AssistantAgent(
    name="assistant",
    instructions="You are a helpful AI assistant.",
    provider=my_provider,
)

result = agent.execute(context)

print(result.output)
```

---

## Example

```python
from bindai_core import (
    AssistantAgent,
    ExecutionContext,
)

context = ExecutionContext()

agent = AssistantAgent(
    name="assistant",
    instructions="You are a helpful AI assistant.",
    provider=my_provider,
)

result = agent.execute(context)

print(result.output)
```

Additional examples are available in the **examples/** directory.

---

## Architecture

```text
                User
                 │
                 ▼
          Assistant Agent
                 │
                 ▼
       Execution Pipeline
                 │
                 ▼
        Model Provider
                 │
                 ▼
        OpenAI / Anthropic
          Ollama / Others
```

---

## Project Structure

```text
bindai/
│
├── packages/
│   ├── bindai-core/
│   ├── bindai-runtime/
│   ├── bindai-tool/
│   └── providers/
│
├── examples/
│
├── playground/
│
├── scripts/
│
├── docs/
│
├── architecture/
│
├── README.md
├── CHANGELOG.md
└── pyproject.toml
```

---

## Current Status

Current release: **v0.1.0**

Implemented

- ✅ Agent framework
- ✅ Assistant agents
- ✅ Provider architecture
- ✅ Provider registry
- ✅ Provider factory
- ✅ Tool framework
- ✅ Automatic tool registration
- ✅ Tool metadata
- ✅ Tool schema generation
- ✅ Conversation management
- ✅ Prompt builder
- ✅ Prompt templates
- ✅ Execution pipeline
- ✅ Middleware
- ✅ Runtime
- ✅ Streaming model responses
- ✅ Playground integration tests

---

## Design Goals

BindAI is built around several core principles.

- Modular architecture
- Provider agnostic
- Extensible components
- Strong typing
- Easy to understand
- Production ready
- Testable
- Lightweight
- Framework-first design

---

## Roadmap

### v0.2

- Native OpenAI provider
- Anthropic provider
- Ollama provider
- Improved tool execution
- Better streaming support
- Tool choice configuration

### v0.3

- Multi-agent orchestration
- Planner agents
- Memory improvements
- Workflow engine
- Workflow visualizer

### v0.4

- MCP support
- Vector memory
- Retrieval-Augmented Generation (RAG)
- Plugin ecosystem
- Knowledge providers

### Future

- Web UI
- Monitoring
- Distributed execution
- Cloud deployment
- Visual workflow editor
- Agent marketplace

---

## Inspiration

BindAI is inspired by ideas from several modern frameworks.

- ASP.NET Core
- Semantic Kernel
- LangGraph
- AutoGen
- FastAPI

The objective is not to replace these projects, but to provide a clean, Python-native framework with a modular architecture and a consistent developer experience.

---

## Testing

The framework currently includes an extensive playground used for validating components during development.

Current status:

- ✅ 30 / 30 playground tests passing

Run all playground tests:

```bash
python scripts/run_playground_tests.py
```

---

## Contributing

Contributions are welcome.

As the project grows, contribution guidelines, coding standards, and development documentation will be added.

For now:

1. Fork the repository.
2. Create a feature branch.
3. Add or update playground tests.
4. Submit a Pull Request.

---

## License

This project is licensed under the **MIT License**.

---

## Version

Current version:

**v0.1.0**

This release establishes the core architecture of BindAI and provides the foundation for future providers, workflows, memory systems, and agent orchestration.

---

<div align="center">

Built with ❤️ using Python.

</div>
