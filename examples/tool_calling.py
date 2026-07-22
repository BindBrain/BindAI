from dotenv import load_dotenv
import os

from bindai import AgentBuilder
from bindai_core.tool import tool

load_dotenv()


@tool()
def add(
    a: int,
    b: int,
):
    """
    Add two integers.
    """

    return a + b


agent = (
    AgentBuilder()
    .openai(
        api_key=os.environ["OPENAI_API_KEY"],
        model="gpt-5",
    )
    .instructions(
        """
        You are a helpful assistant.

        Always use the add tool whenever the user asks for addition.
        Do not perform addition yourself.
        """
    )
    .tool(add)
    .build()
)

result = agent.chat("What is 24 + 18?")

print(result.output)
