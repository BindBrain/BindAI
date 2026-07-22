from bindai import AgentBuilder
from bindai_core.tool import tool


@tool()
def add(a: int, b: int):
    """Add two numbers."""
    return a + b


agent = AgentBuilder().tool(add).build()

result = agent.execute_tool(
    "add",
    a=10,
    b=20,
)

print(result.output)
