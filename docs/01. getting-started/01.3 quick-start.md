# Quick Start

This guide shows how to create and run your first AI agent with BindAI in just a few minutes.

By the end of this guide, you will have:

* Created an AI agent
* Connected it to a language model
* Sent your first prompt
* Received a response

---

# Before You Begin

Make sure you have completed the Installation guide.

You will also need an API key for your chosen model provider.

For OpenAI:

```text id="1x4i90"
OPENAI_API_KEY=your_api_key_here
```

---

# Create an Agent

Create a new file named `main.py`.

```python id="2tmg4w"
from bindai_agent import Agent


agent = Agent(
    provider="openai",
    model="gpt-4.1-mini",
    instructions="You are a helpful assistant.",
)

result = agent.chat(
    "What is BindAI?"
)

print(result.output)
```

Run the file.

```bash id="zh2e3u"
python main.py
```

Example output:

```text id="0l1m1h"
BindAI is a modular Python framework for building AI agents, workflows, tools, memory, and production-ready AI applications.
```

---

# What Happened?

The example performs four simple steps.

## 1. Create an Agent

```python id="tnwt3s"
agent = Agent(
    provider="openai",
    model="gpt-4.1-mini",
    instructions="You are a helpful assistant.",
)
```

This creates a new AI agent configured to use the OpenAI provider and the selected model.

The instructions become the agent's system prompt.

---

## 2. Send a Message

```python id="b85d0e"
result = agent.chat(
    "What is BindAI?"
)
```

The `chat()` method sends your prompt to the configured language model.

---

## 3. Receive the Result

```python id="l6qwdm"
print(result.output)
```

The response returned by the model is available through `result.output`.

---

# Loading an Agent from YAML

Instead of configuring agents in Python, BindAI also supports YAML configuration.

Example:

```yaml id="a0nqqs"
name: assistant

provider: openai

model: gpt-4.1-mini

instructions: |
  You are a helpful assistant.
```

Load the agent.

```python id="ezsfrv"
from pathlib import Path

from bindai_agent import Agent


agent = Agent.from_yaml(
    Path("agent.yaml"),
)

result = agent.chat(
    "Hello!"
)

print(result.output)
```

YAML configuration makes it easier to manage agents without modifying application code.

---

# Using Templates

BindAI includes ready-to-run templates demonstrating common patterns.

Examples include:

* Agent Basics
* Workflow Basics
* Conditions
* Loops
* Parallel Execution
* Retry Policies
* Scheduling

You can execute a template directly.

```bash id="y7e6tv"
python templates/workflow-basic/main.py
```

Templates are the recommended way to learn the framework because every example is fully runnable.

---


