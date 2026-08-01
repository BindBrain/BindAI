<p align="center">
  <a href="https://docs.bindai.dev">
    <img src="logo/light.png" alt="BindAI Logo" width="220">
  </a>
</p>

<h1 align="center">BindAI</h1>

<p align="center">
  Open-source Python framework for building production-ready AI agents, workflows, tools, memory, knowledge retrieval, and enterprise AI applications.
</p>

<p align="center">
  <a href="https://docs.bindai.dev"><strong>Documentation</strong></a> •
  <a href="https://bindai.dev"><strong>Website</strong></a> •
  <a href="https://github.com/BindBrain/BindAI"><strong>GitHub</strong></a>
</p>


# BindAI

> **Open-source Python framework for building production-ready AI agents, workflows, tools, memory, knowledge retrieval, and enterprise AI applications.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-bindai.dev-blue)](https://docs.bindai.dev)

BindAI is a modern Python framework that provides everything you need to build intelligent AI systems using a clean, modular, and provider-agnostic architecture.

Whether you're creating a simple AI assistant, an enterprise workflow, or a complex multi-agent platform, BindAI gives you the building blocks to develop scalable, production-ready AI applications.

---

# Why BindAI?

Modern AI applications require far more than a single LLM call.

BindAI combines:

* AI Agents
* Workflows
* Tools
* Memory
* Knowledge Retrieval (RAG)
* Human Approval Tasks
* Multi-provider LLM support
* Projects
* Templates

into one unified framework.

Everything is modular, extensible, and designed for real-world applications.

---

# Features

## AI Agents

* Intelligent agent execution
* Conversation management
* Prompt management
* Structured outputs
* Tool calling
* Streaming responses

## Workflows

* Visual workflow architecture
* Conditional branching
* Loops
* Parallel execution
* Retry policies
* Timeouts
* Human approval steps
* Scheduling

## Tools

* Automatic tool registration
* Function schema generation
* Tool metadata
* Context-aware execution

## Memory

* Conversation memory
* Custom memory providers
* Extensible memory architecture

## Knowledge

* Document ingestion
* Embeddings
* Vector retrieval
* Retrieval-Augmented Generation (RAG)

## Providers

Provider-agnostic architecture supporting:

* OpenAI
* Anthropic
* Ollama
* Azure OpenAI
* Custom providers

## Projects

Organize multiple applications, workflows, agents, and shared resources inside a single project.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/BindBrain/BindAI.git

cd BindAI
```

Install the framework:

```bash
pip install -e .
```

Or install individual packages during development.

---

# Quick Example

```python
from bindai import Agent

agent = Agent(name="assistant", instructions="You are a helpful AI assistant.")

response = agent.run("Explain what BindAI is.")

print(response.output)
```

---

# Documentation

Complete documentation is available at:

**https://docs.bindai.dev**

Documentation includes:

* Getting Started
* Core Concepts
* Agents
* Tools
* Memory
* Knowledge & RAG
* Workflows
* Projects
* Templates
* API Reference

---

# Templates

BindAI includes ready-to-use templates to accelerate development.

Examples include:

* Basic AI Chat
* AI Assistant
* Workflow Automation
* Human Approval Workflow
* Multi-Agent Systems
* Developer Assistant

Additional templates will continue to be added as the framework evolves.

---

# Architecture

```text
                User
                  │
                  ▼
             AI Agent
                  │
                  ▼
          Execution Engine
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
    Tools                 Workflows
      │                       │
      └───────────┬───────────┘
                  ▼
         Memory & Knowledge
                  │
                  ▼
           Model Providers
                  │
      ┌───────────┴───────────┐
      │                       │
 OpenAI  Anthropic  Ollama  Azure
```

---

# Project Structure

```text
BindAI/

├── packages/
│   ├── bindai/
│   ├── bindai-agent/
│   ├── bindai-core/
│   ├── bindai-memory/
│   ├── bindai-model/
│   ├── bindai-tool/
│   ├── bindai-workflow/
│   ├── bindai-project/
│   └── ...
│
├── docs/
├── templates/
├── examples/
├── scripts/
│
├── docs.json
├── README.md
└── pyproject.toml
```

---

# Roadmap

Upcoming milestones include:

* Additional LLM providers
* Expanded workflow engine
* Enhanced memory systems
* Advanced RAG capabilities
* Visual workflow editor
* Enterprise integrations
* Monitoring & Observability
* Template marketplace
* Plugin ecosystem

---

# Contributing

Contributions are welcome.

If you'd like to improve BindAI:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add tests where appropriate.
5. Submit a Pull Request.

Bug reports, feature requests, and documentation improvements are always appreciated.

---

# Community

* Documentation: https://docs.bindai.dev
* GitHub Issues: https://github.com/BindBrain/BindAI/issues

Additional community channels will be announced in future releases.

---

# License

BindAI is released under the **MIT License**.

---

# Vision

BindAI is designed to become a complete ecosystem for building modern AI software.

The long-term vision is to provide:

* A powerful open-source AI framework
* Production-ready enterprise components
* Installable application templates
* Visual workflow designer
* Complete AI development platform

Build once.

Scale everywhere.

---

<div align="center">

**Built with ❤️ by BindBrain**

https://bindai.dev

</div>
