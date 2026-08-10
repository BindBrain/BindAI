# Build AI Software, Not Just AI Demos

Modern AI applications require far more than a single LLM call.

BindAI provides a unified architecture for building complete AI systems with reusable components for:

* 🤖 AI Agents
* 🔄 Workflows
* 🛠 Tools
* 🧠 Memory
* 📚 Knowledge & RAG
* 📄 Prompt Management
* 🔌 Model Providers
* 🏗 Projects
* ⚙ Enterprise Automation

Whether you're creating an AI assistant, document processing pipeline, internal business automation, or a multi-agent platform, BindAI provides the building blocks to scale from prototype to production-oriented applications.

---

# Installation

Install the complete framework:

```bash
pip install bindai
```

Or clone the repository for development:

```bash
git clone https://github.com/BindBrain/BindAI.git
cd BindAI
pip install -e .
```

---

# Quick Example

```python
from bindai import Agent

agent = Agent(
    name="assistant",
    instructions="You are a helpful AI assistant.",
)

response = agent.run(
    "Explain what BindAI is.",
)

print(response.output)
```

As your application grows, you can incrementally add:

* Memory
* Tools
* Knowledge Retrieval
* Workflows
* Human Approval
* Scheduling
* Multiple AI Providers

without changing the overall application architecture.

---

# Why BindAI?

Most AI frameworks focus on a single part of the application stack.

BindAI is designed as a modular AI application framework where agents, workflows, tools, memory, knowledge, providers, and projects can work together through a consistent architecture.

## Python First

Write clean Python without unnecessary abstractions.

## Modular

Use individual components independently or combine them into larger systems.

## Provider Agnostic

Integrate different model providers without rewriting application-level logic.

## Workflow Orchestration

Build workflows that support sequential execution, conditions, loops, parallel branches, retries, timeouts, human tasks, and scheduled execution.

## Extensible

The package-based architecture allows individual components to evolve independently while remaining part of the larger BindAI ecosystem.

---

# Features

## 🤖 AI Agents

* Intelligent agent execution
* Conversation management
* Prompt management
* Tool calling
* Structured outputs
* Streaming responses

## 🔄 Workflows

BindAI workflows provide an execution engine for coordinating multiple nodes and sharing state through a workflow context.

Supported workflow patterns include:

* Sequential execution
* Conditional branching
* Loops
* Parallel execution
* Human tasks
* Retry policies
* Timeouts
* Scheduling

These patterns can be combined to build more complex business automation.

## 🛠 Tools

* Automatic tool registration
* Function schema generation
* Metadata support
* Context-aware execution

## 🧠 Memory

* Conversation memory
* Pluggable memory providers
* Long-term context

## 📚 Knowledge & RAG

* Document ingestion
* Embeddings
* Vector search
* Retrieval-Augmented Generation

## 🔌 AI Providers

* OpenAI
* Anthropic
* Ollama
* Azure OpenAI
* Custom providers

## 🏗 Projects

Organize applications, workflows, tools, prompts, memory, and knowledge into reusable AI projects.

---

# Package Ecosystem

BindAI is built as a modular package ecosystem.

| Package                  | Purpose                |
| ------------------------ | ---------------------- |
| `bindai`                 | Main framework         |
| `bindai-agent`           | AI agents              |
| `bindai-application`     | Applications           |
| `bindai-cli`             | Command-line interface |
| `bindai-config`          | Configuration          |
| `bindai-core`            | Core framework         |
| `bindai-embeddings`      | Embedding providers    |
| `bindai-group`           | Agent groups           |
| `bindai-host`            | Hosting                |
| `bindai-knowledge`       | Knowledge and RAG      |
| `bindai-memory`          | Memory                 |
| `bindai-model`           | AI models              |
| `bindai-project`         | Project management     |
| `bindai-prompts`         | Prompt system          |
| `bindai-prompt-builder`  | Prompt builder         |
| `bindai-providers`       | Provider interfaces    |
| `bindai-provider-openai` | OpenAI provider        |
| `bindai-retrieval`       | Retrieval              |
| `bindai-runtime`         | Runtime                |
| `bindai-task`            | Tasks                  |
| `bindai-tool`            | Tool system            |
| `bindai-workflow`        | Workflow engine        |

Each package can evolve independently while remaining part of the BindAI ecosystem.

---

# Architecture

```text
                         User
                           │
                           ▼
                        Project
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
          Applications           Workflows
                                      │
                     ┌────────────────┼────────────────┐
                     ▼                ▼                ▼
                  Agents          Conditions        Loops
                     │
             ┌───────┼────────┬──────────┐
             ▼       ▼        ▼          ▼
          Memory  Knowledge  Tools    Providers
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                      OpenAI      Anthropic      Ollama
```

Workflows provide orchestration around agents and other workflow nodes, while the surrounding components provide the capabilities used by those workflows.

---

# Project Structure

```text
BindAI/
│
├── packages/
│   ├── bindai/
│   ├── bindai-agent/
│   ├── bindai-core/
│   ├── bindai-memory/
│   ├── bindai-tool/
│   ├── bindai-workflow/
│   ├── bindai-project/
│   └── ...
│
├── docs/
├── examples/
├── templates/
├── scripts/
│
├── README.md
├── docs.json
└── pyproject.toml
```

---

# Documentation

Complete documentation is available at:

[BindAI Documentation](https://docs.bindai.dev)

The documentation covers:

* Getting Started
* Installation
* Core Concepts
* Agents
* Tools
* Memory
* Knowledge & RAG
* Workflows
* Projects
* Templates
* API Reference

The workflow documentation covers the current execution patterns:

* Workflow Basic
* Workflow Condition
* Workflow Loop
* Workflow Parallel
* Workflow Human
* Workflow Retry
* Workflow Timeout
* Workflow Schedule

The Templates section provides dedicated documentation for these patterns and an overview of how templates are organized.

---

# Roadmap

Planned and ongoing work includes:

* Additional AI providers
* Advanced workflow capabilities
* Enhanced memory systems
* Improved RAG architecture
* MCP integration
* Enterprise integrations
* Monitoring and observability
* Visual workflow editor
* Plugin ecosystem
* Template marketplace

---

# Contributing

Contributions are welcome.

If you'd like to improve BindAI:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add tests when appropriate.
5. Submit a Pull Request.

Bug reports, documentation improvements, and feature suggestions are always appreciated.

---

# Community

* Documentation — [docs.bindai.dev](https://docs.bindai.dev)
* GitHub — [BindAI on GitHub](https://github.com/BindBrain/BindAI)

Community discussions, templates, and additional resources will be introduced as the ecosystem grows.

---

# License

BindAI is released under the **MIT License**.

---

# Vision

BindAI aims to become a complete open-source ecosystem for AI software development.

The long-term vision includes:

* Production-oriented AI framework
* Enterprise automation platform
* Modular package ecosystem
* AI application templates
* Visual workflow designer
* Complete developer platform

---

**Build AI Software. Scale Everywhere.**

Made with ❤️ by **BindBrain**

[bindai.dev](https://bindai.dev)
