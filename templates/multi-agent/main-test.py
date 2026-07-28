from dotenv import load_dotenv

from bindai import Agent
from bindai_provider_openai import OpenAIProvider

load_dotenv()

agent = Agent(
    name="assistant",
    provider=OpenAIProvider(
        model="gpt-4.1-mini",
    ),
    instructions="""
You are a helpful assistant.
""",
)

while True:

    message = input("You: ")

    if message.lower() in {
        "exit",
        "quit",
    }:
        break

    result = agent.chat(
        message,
    )

    print(
        f"Assistant: {result.output}\n",
    )