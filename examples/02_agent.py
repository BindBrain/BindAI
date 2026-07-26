"""
02_agent.py

Learn how to:

- Create an agent using AgentBuilder
- Chat with an LLM
- Understand ExecutionContext
- Understand ModelRequest
- Create a custom Agent
- Create a custom Provider
"""

from bindai import AgentBuilder

from bindai_core.context import ExecutionContext

from bindai_core.model import (
    Message,
    MessageRole,
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ProviderCapabilities,
)

from bindai_core.agent import (
    Agent,
    AgentResult,
)


# ==========================================================
# Example 1 — AgentBuilder
# ==========================================================

print("=" * 60)
print("AgentBuilder")
print("=" * 60)

assistant = (
    AgentBuilder()
    .name("Assistant")
    .instructions(
        "You are a helpful assistant."
    )
    .openai(
        model="gpt-4.1-mini",
    )
    .build()
)

# Requires OPENAI_API_KEY
# Uncomment after configuring environment variables

# result = assistant.chat(
#     "Explain what OpenAI does."
# )
#
# print(result.output)


# ==========================================================
# Example 2 — Execution Context
# ==========================================================

print("\n")
print("=" * 60)
print("ExecutionContext")
print("=" * 60)

context = ExecutionContext()

context.variables.set(
    "company",
    "BindAI",
)

print("Execution ID:", context.execution_id)
print("State:", context.state.value)
print("Company:", context.variables.get("company"))


# ==========================================================
# Example 3 — ModelRequest
# ==========================================================

print("\n")
print("=" * 60)
print("ModelRequest")
print("=" * 60)

request = ModelRequest(
    messages=[
        Message(
            role=MessageRole.USER,
            content="Hello BindAI",
        )
    ]
)

print(request.messages[0].role)
print(request.messages[0].content)


# ==========================================================
# Example 4 — Custom Provider
# ==========================================================

print("\n")
print("=" * 60)
print("Custom Provider")
print("=" * 60)


class DemoProvider(ModelProvider):

    @property
    def name(self):
        return "demo"

    @property
    def capabilities(self):
        return ProviderCapabilities()

    def generate(
        self,
        request,
    ):
        return ModelResponse(
            content="Hello from DemoProvider!",
        )


provider = DemoProvider()

response = provider.generate(request)

print(response.content)


# ==========================================================
# Example 5 — Custom Agent
# ==========================================================

print("\n")
print("=" * 60)
print("Custom Agent")
print("=" * 60)


class HelloAgent(Agent):

    def execute(
        self,
        context,
    ):

        print(f"Running {self.name}")

        return AgentResult(
            success=True,
            output="Finished",
        )


agent = HelloAgent(
    name="Support Agent",
    instructions="You are a helpful assistant.",
    provider=provider,
)

result = agent.execute(
    ExecutionContext(),
)

print(result.output)