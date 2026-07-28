# Project Structure

As AI applications grow, organizing code becomes increasingly important.

BindAI encourages a modular project structure where agents, workflows, tools, memory, and configuration are separated into dedicated directories.

The exact layout is flexible, but the following structure is recommended for most applications.

---

# Recommended Layout

```text
my-ai-project/

├── .env
├── requirements.txt
├── main.py
│
├── agents/
│   ├── assistant.yaml
│   ├── researcher.yaml
│   └── support.yaml
│
├── workflows/
│   ├── customer_support.py
│   ├── research.py
│   └── approval.py
│
├── tools/
│   ├── calculator.py
│   ├── weather.py
│   └── database.py
│
├── memory/
│   └── provider.py
│
├── knowledge/
│   ├── documents/
│   └── embeddings/
│
├── applications/
│   ├── chatbot.py
│   └── support.py
│
├── templates/
│
└── tests/
```

This structure keeps each concern isolated while remaining easy to extend.

---

# Directory Overview

## agents/

Contains agent configuration files.

Typical contents:

* system instructions
* model configuration
* provider configuration
* tools
* memory
* knowledge

Example:

```text
agents/
    assistant.yaml
```

---

## workflows/

Contains workflow definitions.

Examples include:

* customer onboarding
* research automation
* approval flows
* scheduled jobs

Each workflow orchestrates one or more agents.

---

## tools/

Contains reusable Python tools.

Examples:

* API clients
* calculators
* search utilities
* database access
* external integrations

Tools can be shared across multiple agents.

---

## memory/

Contains memory providers.

Examples:

* in-memory provider
* Redis
* PostgreSQL
* custom implementations

---

## knowledge/

Stores documents and retrieval resources.

Typical contents include:

* PDFs
* Markdown files
* embeddings
* vector indexes

These resources are used by retrieval-augmented generation (RAG).

---

## applications/

Applications combine agents, workflows, and tools into complete AI systems.

For example:

```python
project
    ↓
application
    ↓
agents
    ↓
tools
```

One project can contain multiple independent applications.

---

## templates/

Contains runnable examples demonstrating BindAI features.

Templates are intended as learning resources and starting points for new projects.

---

## tests/

Contains automated tests for your project.

Testing agents, workflows, and tools independently helps keep applications reliable as they grow.

---

# Scaling Projects

A small project may only contain:

```text
main.py

agent.yaml
```

As additional functionality is introduced, new directories can be added without changing the overall architecture.

This allows projects to grow naturally while remaining organized.

---

# Large Projects

Enterprise applications often contain multiple agents and workflows.

Example:

```text
project

├── applications/
│   ├── support/
│   ├── sales/
│   └── research/
│
├── agents/
│   ├── assistant.yaml
│   ├── researcher.yaml
│   ├── reviewer.yaml
│   └── manager.yaml
│
├── workflows/
│   ├── onboarding.py
│   ├── approval.py
│   ├── research.py
│   └── reporting.py
```

This separation allows teams to develop different parts of the application independently.

---

# Configuration

Sensitive values should never be stored in source code.

Instead, place configuration inside environment variables.

Example:

```text
OPENAI_API_KEY=...
```

Agent behavior should generally live inside YAML configuration files rather than Python code whenever possible.

---

# Best Practices

* Keep agents focused on a single responsibility.
* Reuse tools across multiple agents.
* Store prompts in YAML files.
* Organize workflows by business process.
* Keep application logic separate from workflow logic.
* Write tests for custom tools and workflows.
* Use templates as starting points instead of modifying framework code.


