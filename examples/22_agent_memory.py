"""
22. Agent Memory

Demonstrates an agent keeping
conversation memory between turns.
"""

from bindai import AgentBuilder

agent = (
    AgentBuilder()
    .instructions(
        """
        You are a helpful assistant.
        Remember information the user gives you.
        """
    )
    .build()
)


print("=" * 60)
print("BindAI Agent Memory Demo")
print("=" * 60)


conversation = [
    "My name is Alex.",
    "I work on AI agent frameworks.",
    "What is my name?",
    "What do I work on?",
]


for message in conversation:
    print("\nUser:")
    print(message)

    result = agent.chat(message)

    print("\nAssistant:")
    print(result.output)
