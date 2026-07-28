# First Agent

In BindAI, an **Agent** is the core building block of every AI application.

An agent connects a language model with instructions, tools, memory, knowledge, and workflows to perform useful tasks.

This guide explains how agents work and how to build your own.

---

# What is an Agent?

An agent is responsible for:

* Receiving user input
* Building a prompt
* Sending the request to a language model
* Executing tools when required
* Returning the final response

Unlike calling an LLM directly, a BindAI agent can be extended with additional capabilities while keeping the application architecture clean.

---

# Creating an Agent

The simplest agent only requires a provider, model, and instructions.

```python
from bindai_agent import Agent


agent = Agent(
    provider="openai",
    model="gpt-4.1-mini",
    instructions="You are a helpful assistant.",
)
```

You can immediately interact with it.

```python
result = agent.chat(
    "Explain artificial intelligence in one sentence."
)

print(result.output)
```

---

# Agent Components

A BindAI agent is composed of several optional building blocks.

| Component    | Purpose                                         |
| ------------ | ----------------------------------------------- |
| Provider     | Connects to an LLM provider such as OpenAI      |
| Model        | Specifies which language model to use           |
| Instructions | Defines the agent's behavior                    |
| Tools        | Allows the model to execute Python functions    |
| Memory       | Stores previous conversations                   |
| Knowledge    | Supplies external documents and information     |
| Middleware   | Executes logic before and after agent execution |
| Events       | Publishes lifecycle events during execution     |

You can start with only a provider and model, then add more capabilities as your application grows.

---

# System Instructions

Instructions define the agent's personality and behavior.

```python
agent = Agent(
    provider="openai",
    model="gpt-4.1-mini",
    instructions="""
You are an experienced Python mentor.
Always explain concepts clearly.
Keep answers concise.
""",
)
```

Good instructions usually describe:

* The agent's role
* Desired writing style
* Constraints
* Expected output format

---

# Sending Messages

Use the `chat()` method to send a prompt.

```python
result = agent.chat(
    "What is dependency injection?"
)
```

The returned value is an `AgentResult`.

```python
print(result.success)

print(result.output)
```

Typical output:

```text
True

Dependency injection is a design pattern where dependencies are supplied from the outside instead of being created internally.
```

---

# Structured Output

Agents can also return structured data.

Suppose you have a Pydantic model.

```python
from pydantic import BaseModel


class Person(BaseModel):

    name: str

    age: int
```

Pass it as the `output` argument.

```python
result = agent.chat(
    "Generate a fictional person.",
    output=Person,
)

print(result.output)
```

The response becomes an instance of your model instead of plain text.

---

# Loading Agents from YAML

Agents can be defined without writing Python code.

Example configuration:

```yaml
name: assistant

provider: openai

model: gpt-4.1-mini

instructions: |
  You are a helpful assistant.
```

Load it.

```python
from pathlib import Path

from bindai_agent import Agent


agent = Agent.from_yaml(
    Path("agent.yaml"),
)
```

YAML is useful for production projects where prompts and models change frequently.

---

# Streaming Responses

Instead of waiting for the complete answer, responses can be streamed token by token.

```python
for chunk in agent.stream(
    "Explain neural networks."
):
    print(chunk.delta, end="")
```

Streaming is recommended for chat interfaces and long responses.

---

# Agent Lifecycle

Internally, every execution follows the same pipeline.

1. Receive user input
2. Build the prompt
3. Load memory
4. Retrieve knowledge (if configured)
5. Send the request to the language model
6. Execute requested tools
7. Generate the final response
8. Save conversation memory
9. Return an `AgentResult`

This lifecycle remains the same regardless of whether the agent uses tools, workflows, or retrieval.

---

# Extending an Agent

Agents become more powerful by adding additional capabilities.

For example, register a tool.

```python
agent.tool(
    weather_tool,
)
```

Attach memory.

```python
agent.use_memory(
    memory,
)
```

Connect knowledge retrieval.

```python
agent.use_knowledge(
    knowledge,
)
```

These extensions allow the same agent architecture to support increasingly complex applications.

