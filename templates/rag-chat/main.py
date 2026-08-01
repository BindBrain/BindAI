from pathlib import Path

from bindai import Agent
from bindai_knowledge import (
    DirectoryLoader,
    InMemoryKnowledgeProvider,
    Knowledge,
)
from dotenv import load_dotenv

load_dotenv()

BASE = Path(__file__).parent

agent = Agent.from_yaml(BASE / "agent.yaml")

knowledge = Knowledge(
    InMemoryKnowledgeProvider(),
)

knowledge.load(
    DirectoryLoader(
        BASE / "knowledge",
    )
)

agent.use_knowledge(
    knowledge,
)

print("BindAI RAG Chat")
print("Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    if message.lower() in {"exit", "quit"}:
        break

    result = agent.chat(message)

    print(f"\nAssistant: {result.output}\n")
