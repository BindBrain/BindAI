# BindAI Documentation

Welcome to the official documentation for **BindAI**.

BindAI is an open-source Python framework for building production-ready AI applications using agents, workflows, tools, memory, knowledge retrieval, model providers, projects, external integrations, and multi-agent systems.

The framework provides a modular architecture that can scale from simple AI assistants and tool-calling applications to complex agentic workflows and automation systems.

---

# What is BindAI?

BindAI is built around a modular set of components:

* AI Agents
* Tools
* Model Providers
* Memory
* Knowledge and RAG
* Embeddings
* Retrieval
* Workflows
* Projects
* Connections and Integrations
* MCP
* Multi-Agent Systems

These components are designed to work together while remaining modular and independently extensible.

---

# Documentation

## Getting Started

Learn how to install BindAI and build your first AI application.

* Introduction
* Installation
* Quick Start
* First Agent
* Project Structure

---

## Core

Understand the main building blocks of BindAI.

* Agents
* Prompts
* Agent Execution
* Providers
* Results
* Events
* Agent Configuration
* Conversation Management
* Tool Execution
* Hooks, Callbacks, and Middleware
* Agent Delegation
* Multi-Agent Execution

---

## Tools

Learn how to create and execute tools that can be used by BindAI agents.

Topics include:

* Tool Overview
* Creating Tools
* Tool Context
* Tool Results
* Tool Calling
* Multiple Tools
* Tool Registry and Execution

Tools can also be connected to external systems and MCP services.

---

## Memory

Learn how BindAI stores and retrieves conversation and application memory.

Current memory capabilities include:

* In-Memory Memory
* SQLite
* PostgreSQL
* Pinecone
* Chroma
* Vector Memory
* Conversation Memory
* Custom Memory Providers
* Memory Abstractions

Additional storage and retrieval providers are planned.

---

## Knowledge and RAG

Build knowledge-powered AI applications using retrieval-augmented generation.

Current capabilities include:

* Document Loading
* Document Ingestion
* Parsing
* Chunking
* Embeddings
* Metadata
* Semantic Retrieval
* BM25 Retrieval
* Hybrid Retrieval
* Filtering
* Reranking
* Lexical Reranking
* Conversational Retrieval
* Knowledge Pipelines
* Agent Knowledge Integration

BindAI provides abstractions for building knowledge systems ranging from local retrieval to production-scale RAG pipelines.

---

## Workflows

Learn how BindAI workflows execute nodes, share execution context, and coordinate advanced execution patterns.

The workflow documentation covers:

* Workflow Basics
* Workflow Builder
* Nodes
* Conditions
* Loops
* Parallel Execution
* Retry Policies
* Timeouts
* Scheduling
* Human Tasks

These patterns can be combined to build reliable workflow execution, AI-driven processes, and business automation.

---

## Projects

Organize applications, agents, workflows, and shared resources inside a project.

Topics include:

* Project Structure
* Applications
* Shared Tools
* Configuration
* Deployment

Projects provide a higher-level structure for organizing BindAI applications.

---

## Templates

The Templates documentation provides examples of common BindAI patterns and workflow configurations.

The workflow template documentation currently includes:

* Workflow Basic
* Workflow Condition
* Workflow Loop
* Workflow Parallel
* Workflow Human
* Workflow Retry
* Workflow Timeout
* Workflow Schedule
* Templates Overview

Templates provide practical starting points for understanding how BindAI workflow capabilities fit together.

---

## Connections

The Connections documentation covers integrations between BindAI and external services.

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

The Connections package provides a common connection abstraction, registry, and connection manager so integrations can be implemented consistently.

Additional integrations are planned.

---

## MCP

BindAI includes Model Context Protocol support for connecting agents and tools to MCP-compatible services.

Current MCP capabilities include:

* MCP Client Connections
* Tool Discovery
* Tool Calling
* MCP Tools as BindAI Tools
* Basic MCP Connection Handling

Additional MCP capabilities, including resource discovery, authentication, advanced connection management, and expanded protocol support, are planned.

---

## Multi-Agent Systems

BindAI supports agent delegation and multi-agent execution patterns.

Current capabilities include:

* Agent Delegation
* Agent Handoff
* Specialist Agents
* Team Delegation
* Specialist Role Chains
* RAG-Enabled Agents
* Structured Agent Configuration
* Agent Execution Configuration

Advanced planning, supervisor agents, hierarchical coordination, and more advanced multi-agent state management remain under development.

---

## API Reference

Detailed reference documentation for the main BindAI APIs.

Current API reference areas include:

* Agents
* Workflows
* Projects
* Tools
* Memory
* Providers

The API reference will expand as additional public APIs and packages are stabilized.

---

# Documentation Structure

The documentation is organized into numbered sections covering the major areas of BindAI.

```text
docs/
│
├── README.md
├── CHECKLIST.md
├── ROADMAP.md
│
├── 01. getting-started/
├── 02. core/
├── 03. tools/
├── 04. memory/
├── 05. knowledge/
├── 06. workflows/
├── 07. projects/
├── 08. templates/
├── 09. connections/
└── 10. api/
```

The exact contents of each section may grow as additional BindAI features are implemented and documented.

---

# Current Development Status

BindAI is actively under development.

The current implementation provides a substantial foundation for:

* AI agents
* Tool calling
* Model provider integrations
* Memory
* Knowledge and RAG
* Embeddings
* Vector, lexical, and hybrid retrieval
* Workflow orchestration
* Conditional execution
* Loops
* Parallel execution
* Retries and timeouts
* Human tasks
* Scheduling
* Projects
* Agent delegation
* Multi-agent teams and specialist role chains
* External service connections
* MCP tool integration

Additional providers, storage backends, integrations, advanced multi-agent coordination, automation infrastructure, deployment capabilities, and observability features remain under development.

See the **ROADMAP** for the detailed implementation status and planned development.

---

# Recommended Learning Path

If you're new to BindAI, a recommended learning path is:

1. Installation
2. Quick Start
3. First Agent
4. Core Concepts
5. Tools
6. Memory
7. Knowledge and RAG
8. Workflows
9. Projects
10. Connections
11. MCP
12. Templates
13. API Reference

Start with the fundamentals, then explore tools, memory, knowledge, workflows, and integrations as your application grows.

---

# Need Help?

The BindAI documentation evolves alongside the framework.

For the current implementation status, planned features, and long-term direction, see the **ROADMAP**.

Happy building with BindAI.
