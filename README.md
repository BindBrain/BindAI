<p align="center">
  <a href="https://bindai.dev">
    <img src="logo/light.png" alt="BindAI Logo" width="220">
  </a>
</p>

<h1 align="center">BindAI</h1>

<p align="center">
  <strong>Build production-ready AI applications with agents, workflows, memory, knowledge retrieval, and tools.</strong>
</p>

<p align="center">
  A modular, provider-agnostic Python framework for developing intelligent applications—from AI assistants to enterprise automation platforms.
</p>

<p align="center">
  <a href="https://docs.bindai.dev"><strong>Documentation</strong></a> •
  <a href="https://bindai.dev"><strong>Website</strong></a> •
  <a href="https://pypi.org/project/bindai/"><strong>PyPI</strong></a> •
  <a href="https://github.com/BindBrain/BindAI"><strong>GitHub</strong></a>
</p>

---

# Build AI Software, Not Just AI Demos

Modern AI applications require far more than a single LLM call.

BindAI provides a unified architecture for building complete AI systems with reusable components for:

- 🤖 AI Agents
- 🔄 Workflows
- 🛠 Tools
- 🧠 Memory
- 📚 Knowledge & RAG
- 📄 Prompt Management
- 🔌 Model Providers
- 🏗 Projects
- ⚙ Enterprise Automation

Whether you're creating an AI assistant, document processing pipeline, internal business automation, or a distributed multi-agent platform, BindAI provides the building blocks to scale from prototype to production.

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
    instructions="You are a helpful AI assistant."
)

response = agent.run(
    "Explain what BindAI is."
)

print(response.output)
```

As your application grows you can incrementally add:

- Memory
- Tools
- Knowledge Retrieval
- Workflows
- Human Approval
- Scheduling
- Multiple AI Providers

without changing your application's architecture.

---

# Why BindAI?

Most AI frameworks focus on a single part of the problem.

BindAI is designed as a complete application framework where every component works together through a consistent architecture.

## Python First

Write clean Python without excessive abstractions.

## Modular

Every component can be used independently or combined into larger systems.

## Provider Agnostic

Switch between OpenAI, Anthropic, Ollama, Azure OpenAI, and future providers without rewriting application logic.

## Production Ready

Designed for real-world software with retries, workflows, scheduling, memory, logging, and extensibility.

---

# Features

## 🤖 AI Agents

- Intelligent agent execution
- Conversation management
- Prompt management
- Tool calling
- Structured outputs
- Streaming responses

## 🔄 Workflows

- Sequential execution
- Conditional branching
- Loops
- Parallel execution
- Retry policies
- Timeouts
- Human approval
- Scheduling

## 🛠 Tools

- Automatic tool registration
- Function schema generation
- Metadata support
- Context-aware execution

## 🧠 Memory

- Conversation memory
- Pluggable memory providers
- Long-term context

## 📚 Knowledge & RAG

- Document ingestion
- Embeddings
- Vector search
- Retrieval-Augmented Generation

## 🔌 AI Providers

- OpenAI
- Anthropic
- Ollama
- Azure OpenAI
- Custom Providers

## 🏗 Projects

Organize applications, workflows, tools, prompts, memory, and knowledge into reusable AI projects.

---

# Package Ecosystem

BindAI is built as a modular ecosystem.

| Package | Purpose |
|----------|----------|
| bindai | Main framework |
| bindai-agent | AI Agents |
| bindai-application | Applications |
| bindai-cli | Command Line Interface |
| bindai-config | Configuration |
| bindai-core | Core Framework |
| bindai-embeddings | Embedding Providers |
| bindai-group | Agent Groups |
| bindai-host | Hosting |
| bindai-knowledge | Knowledge & RAG |
| bindai-memory | Memory |
| bindai-model | AI Models |
| bindai-project | Project Management |
| bindai-prompts | Prompt System |
| bindai-prompt-builder | Prompt Builder |
| bindai-providers | Provider Interface |
| bindai-provider-openai | OpenAI Provider |
| bindai-retrieval | Retrieval |
| bindai-runtime | Runtime |
| bindai-task | Tasks |
| bindai-tool | Tool System |
| bindai-workflow | Workflow Engine |

Each package can evolve independently while remaining fully compatible with the BindAI ecosystem.

---

# Architecture

```text
                 User
                   │
                   ▼
                Project
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
    Applications        Workflows
         │                   │
         └─────────┬─────────┘
                   ▼
                 Agents
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Memory    Knowledge    Tools
        │          │          │
        └──────────┼──────────┘
                   ▼
             Model Providers
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
   OpenAI     Anthropic      Ollama
```

Every component has a single responsibility, making applications easier to extend, test, and maintain.

---

# Project Structure

```text
BindAI/

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

**https://docs.bindai.dev**

Documentation includes:

- Getting Started
- Installation
- Core Concepts
- Agents
- Tools
- Memory
- Knowledge & RAG
- Workflows
- Projects
- Templates
- API Reference

---

# Roadmap

Upcoming milestones include:

- Additional AI providers
- Advanced workflow engine
- Enhanced memory systems
- Improved RAG architecture
- MCP integration
- Enterprise integrations
- Monitoring & Observability
- Visual workflow editor
- Plugin ecosystem
- Template marketplace

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

- Documentation — https://docs.bindai.dev
- GitHub Issues — https://github.com/BindBrain/BindAI/issues

Community discussions, templates, and additional resources will be introduced as the ecosystem grows.

---

# License

BindAI is released under the **MIT License**.

---

# Vision

BindAI aims to become a complete open-source ecosystem for AI software development.

The long-term vision includes:

- Production-ready AI framework
- Enterprise automation platform
- Modular package ecosystem
- AI application templates
- Visual workflow designer
- Complete developer platform

---

<p align="center">

**Build AI Software. Scale Everywhere.**

Made with ❤️ by **BindBrain**

https://bindai.dev

</p>