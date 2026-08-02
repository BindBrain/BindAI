from bindai import AgentBuilder, tool

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

print()


#
# Execute manually
#

print("=== Direct Execution ===")

result = add(
    a=10,
    b=20,
)

print(result)

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
    .tools(add.function)
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

print(tool_result.value)

print()


#
# LLM Tool Calling
#

print("=== LLM Tool Calling ===")

response = agent.chat("What is 24891 + 91742?")

print("Success:", response.success)
print("Response:")
print(response.output)
