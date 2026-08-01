from pathlib import Path

from bindai import Agent
from dotenv import load_dotenv

from tools import current_time

load_dotenv()

template_dir = Path(__file__).parent

agent = Agent.from_yaml(
    template_dir / "agent.yaml",
)

agent.tool(current_time)

print("BindAI Tool Agent")
print("Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    if message.lower() in {"exit", "quit"}:
        break

    result = agent.chat(message)

    print(f"\nAssistant: {result.output}\n")
