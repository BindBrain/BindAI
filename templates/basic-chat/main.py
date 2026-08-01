from pathlib import Path

from bindai import Agent
from dotenv import load_dotenv

load_dotenv()

template_dir = Path(__file__).parent

agent = Agent.from_yaml(
    template_dir / "agent.yaml",
)

print("BindAI Basic Chat")
print("Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    if message.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break

    result = agent.chat(message)

    print(f"Assistant: {result.output}\n")
