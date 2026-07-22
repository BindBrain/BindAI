from dotenv import load_dotenv
import os

from bindai import AgentBuilder

load_dotenv()

agent = (
    AgentBuilder()
    .openai(
        api_key=os.environ["OPENAI_API_KEY"],
        model="gpt-5",
    )
    .instructions("You are a helpful assistant.")
    .build()
)

result = agent.chat("Hello!")

print(result.output)
