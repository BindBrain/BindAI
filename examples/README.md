# BindAI Examples

These examples demonstrate the major capabilities of BindAI, from simple AI agents to production-ready AI applications.

The examples are organized progressively:

- Start with basic agents
- Learn tools, memory, and knowledge
- Build workflows and multi-agent systems
- Integrate BindAI into real applications
- Explore advanced production patterns

---

# Getting Started

All examples can be executed from the repository root:

```bash
python examples/<example>.py
```

Example:

```bash
python examples/01_hello_world.py
```

Install project dependencies first:

```bash
uv sync
```

---

# Example Index

| # | Example | Description |
|---|---------|-------------|
| 01 | Hello World | Your first BindAI agent |
| 02 | Building an Agent | Configure models, prompts, and agent behavior |
| 03 | Using Tools | Create and register custom tools |
| 04 | Streaming | Stream AI responses in real time |
| 05 | Memory | Build persistent conversational memory |
| 06 | Knowledge | Use Retrieval-Augmented Generation (RAG) |
| 07 | Events | Observe agent execution events |
| 08 | Workflows | Build multi-step AI workflows |
| 09 | Multi-Agent Groups | Coordinate multiple AI agents |
| 10 | YAML Configuration | Configure BindAI applications with YAML |
| 11 | Custom Providers | Integrate custom LLM providers |
| 12 | Custom Tools | Build reusable tool integrations |
| 13 | Structured Output | Return validated structured objects |
| 14 | RAG Chatbot | Build a knowledge-powered assistant |
| 15 | Multi-Agent Research | Research using multiple specialized agents |
| 16 | Parallel Workflow | Execute workflow tasks concurrently |
| 17 | Human Approval | Build human-in-the-loop workflows |
| 18 | Retry & Timeout | Add workflow reliability and error recovery |
| 19 | FastAPI Integration | Expose BindAI through REST APIs |
| 20 | CLI Assistant | Build an interactive terminal assistant |
| 21 | Document QA | Answer questions over documents |
| 22 | Workflow Builder | Create workflows programmatically |
| 23 | MCP Tool Integration | Connect external MCP tools |
| 24 | Custom Memory Provider | Create custom memory backends |
| 25 | Custom Embedding Provider | Add custom embedding systems |
| 26 | Vector Database Integration | Connect external vector storage |
| 27 | Scheduled Agent | Run agents on schedules |
| 28 | Event Driven Agent | Trigger agents from events |
| 29 | Production Project Layout | Organize a production AI application |
| 30 | Full AI Application | Complete production-style BindAI application |

---

# File Mapping

| Example | File |
|---------|------|
| 01 | `01_hello_world.py` |
| 02 | `02_agent.py` |
| 03 | `03_tools.py` |
| 04 | `04_streaming.py` |
| 05 | `05_memory.py` |
| 06 | `06_knowledge.py` |
| 07 | `07_events.py` |
| 08 | `08_workflow.py` |
| 09 | `09_group.py` |
| 10 | `10_yaml.py` |
| 11 | `11_custom_provider.py` |
| 12 | `12_custom_tool.py` |
| 13 | `13_structured_output.py` |
| 14 | `14_rag_chatbot.py` |
| 15 | `15_multi_agent_research.py` |
| 16 | `16_parallel_workflow.py` |
| 17 | `17_human_approval.py` |
| 18 | `18_retry_timeout.py` |
| 19 | `19_fastapi.py` |
| 20 | `20_cli_assistant.py` |
| 21 | `21_document_qa.py` |
| 22 | `22_workflow_builder.py` |
| 23 | `23_mcp_tools.py` |
| 24 | `24_custom_memory.py` |
| 25 | `25_custom_embeddings.py` |
| 26 | `26_vector_database.py` |
| 27 | `27_scheduled_agent.py` |
| 28 | `28_event_agent.py` |
| 29 | `29_production_layout.py` |
| 30 | `30_full_application.py` |

---

# Basic Agents

## 01 Hello World

Learn the basics:

- Creating your first agent
- Running prompts
- Receiving responses

---

## 02 Building an Agent

Learn how to configure:

- Models
- System prompts
- Agent behavior
- Runtime options

---

## 03 Using Tools

Create agents that can:

- Execute functions
- Call external services
- Use custom capabilities

---

## 04 Streaming

Learn:

- Token streaming
- Real-time responses
- Interactive applications

---

# Memory & Knowledge

## 05 Memory

Examples include:

- Conversation history
- Persistent context
- Memory providers

---

## 06 Knowledge

Learn:

- Document ingestion
- Retrieval
- Embeddings
- RAG pipelines

---

## 14 RAG Chatbot

Build a complete knowledge assistant:

```text
Documents
    |
    v
Knowledge Base
    |
    v
Retriever
    |
    v
AI Agent
    |
    v
Answer
```

---

## 21 Document QA

Question answering over private documents.

Demonstrates:

- Document loading
- Retrieval
- Context-aware answers

---

# Workflows

## 08 Workflows

Introduction to:

- Workflow nodes
- Tasks
- Execution flow

---

## 16 Parallel Workflow

Execute independent workflow tasks concurrently.

```text
             Workflow
                |
       +--------+--------+
       |                 |
       v                 v
 Research Task     Analysis Task
       |                 |
       +--------+--------+
                |
                v
             Result
```

---

## 17 Human Approval

Create workflows requiring human decisions.

Use cases:

- Production deployments
- Business approvals
- Safety checks

---

## 18 Retry & Timeout

Production reliability features:

- Retry failed operations
- Handle temporary failures
- Protect long-running tasks

---

## 22 Workflow Builder

Build workflows directly in Python.

Features:

- Task composition
- Context passing
- Reusable pipelines

---

# Multi-Agent Systems

## 09 Multi-Agent Groups

Coordinate multiple agents.

Examples:

- Research teams
- Specialist agents
- Collaborative systems

---

## 15 Multi-Agent Research

Create a research team:

```text
Research Agent
       |
       v
Analysis Agent
       |
       v
Writing Agent
       |
       v
Final Report
```

---

# Application Integration

## 19 FastAPI Integration

Expose BindAI through APIs.

Demonstrates:

- REST endpoints
- Backend services
- Production integration

---

## 20 CLI Assistant

Build:

- Terminal assistants
- Developer tools
- Interactive AI applications

---

# Advanced Integrations

## 10 YAML Configuration

Configure applications without writing Python.

---

## 11 Custom Providers

Create integrations for:

- New LLM providers
- Internal models
- Enterprise systems

---

## 12 Custom Tools

Build reusable capabilities:

- APIs
- Database access
- External services

---

## 13 Structured Output

Return:

- Typed objects
- Validated responses
- Reliable application data

---

## 23 MCP Tool Integration

Connect BindAI with external Model Context Protocol tools.

Demonstrates:

- MCP client connection
- Tool discovery
- External tool execution
- Agent integration

Example flow:

```text
MCP Server
     |
     v
MCP Client
     |
     v
BindAI Agent
     |
     v
Tool Execution
     |
     v
Response

---

## 24 Custom Memory Provider

Create custom memory implementations.

Demonstrates:

- Memory interfaces
- Custom storage backends
- Conversation persistence
- External database integration

Example flow:

```text
User Message
      |
      v
Custom Memory Provider
      |
      v
Storage Backend
      |
      v
Agent Context

---

## 25 Custom Embedding Provider

Implement custom embedding systems.

Demonstrates:

- Embedding interfaces
- Vector generation
- Similarity calculations
- Custom model integration

Example flow:

```text
Text Input
    |
    v
Embedding Provider
    |
    v
Vector Representation
    |
    v
Similarity Search

---

## 26 Vector Database Integration

Connect external vector storage systems.

Demonstrates:

- Document indexing
- Vector storage
- Similarity search
- Retrieval pipelines

Example flow:

```text
Documents
    |
    v
Embedding Provider
    |
    v
Vector Database
    |
    v
Similarity Search
    |
    v
Retrieved Context

---

## 27 Scheduled Agent

Run AI agents automatically on schedules.

Demonstrates:

- Scheduled execution
- Background agents
- Automated workflows
- Periodic reporting

Example flow:

```text
Scheduler
    |
    v
AI Agent
    |
    v
Task Execution
    |
    v
Generated Report

---

## 28 Event Driven Agent

Trigger AI agents from external events.

Demonstrates:

- Event listeners
- Agent triggers
- Event payload processing
- Automated reactions

Example flow:

```text
External Event
      |
      v
Event Bus
      |
      v
AI Agent
      |
      v
Action / Response

---

# Production Applications

## 29 Production Project Layout

Recommended structure for production BindAI applications.

Demonstrates:

- Application organization
- Separation of concerns
- Modular architecture
- Scalable project layout

Example:

```text
my-bindai-application/

├── agents/
├── workflows/
├── tools/
├── memory/
├── knowledge/
├── config/
├── api/
├── tests/
└── main.py

## 30 Full AI Application

Complete production-style BindAI application demonstrating:

Architecture:

User
 |
 v
Application
 |
 +---- Agent
 |
 +---- Tools
 |
 +---- Memory
 |
 +---- Knowledge
 |
 +---- Workflow
 |
 v
Response


Features:

- Agent orchestration
- Business tools
- Persistent memory
- Workflow execution
- Production project patterns

---

# Example Assets

Additional files:

```text
examples/

├── assets/
│   ├── marketing.yaml
│   └── research_group.yaml
```

These assets are used by:

- YAML configuration examples
- Multi-agent examples
- Workflow examples

---

# Requirements

Base examples:

```bash
uv sync
```

Optional integrations may require:

```bash
pip install fastapi uvicorn
```

Provider examples may require API keys:

```bash
export OPENAI_API_KEY="your-key"
```

---

# Running Examples

Run a single example:

```bash
python examples/01_hello_world.py
```

Run examples individually:

```bash
python examples/<file>.py
```

---

# Recommended Learning Path

## New Users

```text
01 → 02 → 03 → 05 → 06 → 08
```

## Developers Building Applications

```text
02 → 03 → 06 → 08 → 14 → 19
```

## Advanced Users

```text
15 → 16 → 17 → 18 → 23 → 30
```

---

# Contributing Examples

When adding a new example:

- Keep it focused on one feature
- Add comments explaining concepts
- Update this README
- Include required dependencies
- Ensure it runs independently

---

Happy building with **BindAI** 🚀