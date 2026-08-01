from bindai import AgentBuilder
from bindai_core.tool import tool

#
# Create a tool
#


@tool()
def add(a: int, b: int):
    """
    Add two integers.
    """
    return a + b


#
# Inspect metadata
#

print("=== Tool Metadata ===")

print(add.name)
print(add.description)
print(add.parameters)

print()


#
# Execute manually
#

print("=== Direct Execution ===")

result = add.execute(
    a=10,
    b=20,
)

print(result.output)

print()


#
# Register with an agent
#

agent = (
    AgentBuilder()
    .name("Math Assistant")
    .instructions(
        """
        You are a helpful assistant.

        Always use the add tool whenever the user asks for addition.
        """
    )
    .tool(add)
    .openai(
        model="gpt-4.1-mini",
    )
    .build()
)

print("=== Manual Agent Tool Execution ===")

tool_result = agent.execute_tool(
    "add",
    a=25,
    b=35,
)

print(tool_result.output)

print()


#
# LLM Tool Calling
#

print("=== LLM Tool Calling ===")

response = agent.chat("What is 24891 + 91742?")

print("Success:", response.success)
print("Iterations:", response.iterations)
print("Response:")
print(response.response)
