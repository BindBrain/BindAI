from bindai_agent import AgentBuilder
from bindai_tool import tool


@tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


agent = (
    AgentBuilder()
    .openai("gpt-5")
    .tool(add)
    .build()
)

result = agent.chat(
    "What is 12 + 30?"
)

print(result.response)