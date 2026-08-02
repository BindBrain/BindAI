"""
24 Custom Memory Provider

Demonstrates creating a custom memory backend.

Concepts:
- Custom memory implementation
- Memory interface
- Storing conversation history
- Retrieving previous context
"""

from typing import Any

from bindai import AgentBuilder


class SimpleMemory:
    """
    Example custom in-memory storage.

    A production implementation could use:
    - Redis
    - PostgreSQL
    - MongoDB
    - Cloud storage
    """

    def __init__(self):
        self.storage: dict[str, list[dict[str, Any]]] = {}

    def save(
        self,
        user_id: str,
        role: str,
        content: str,
    ):
        if user_id not in self.storage:
            self.storage[user_id] = []

        self.storage[user_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def history(
        self,
        user_id: str,
    ):
        return self.storage.get(
            user_id,
            [],
        )


class CustomMemoryProvider:
    """
    Adapter exposing custom memory
    to BindAI.
    """

    def __init__(self):
        self.memory = SimpleMemory()

    def add_message(
        self,
        user_id: str,
        role: str,
        content: str,
    ):
        self.memory.save(
            user_id,
            role,
            content,
        )

    def get_messages(
        self,
        user_id: str,
    ):
        return self.memory.history(user_id)


def main():

    memory = CustomMemoryProvider()

    user_id = "demo-user"

    memory.add_message(
        user_id,
        "user",
        "My name is Alex.",
    )

    context = memory.get_messages(user_id)

    print("Stored memory:")
    for message in context:
        print(message)

    agent = (
        AgentBuilder()
        .openai("gpt-4.1-mini")
        .instructions(
            """
            You are an assistant that
            uses conversation memory.

            Always use the provided memory
            when answering questions.
            """
        )
        .build()
    )

    memory_text = "\n".join([f"{m['role']}: {m['content']}" for m in context])

    prompt = f"""
Previous conversation memory:

{memory_text}


Question:
What is my name?
"""

    result = agent.chat(prompt)

    print("\nAgent response:")
    print(result.output)


if __name__ == "__main__":
    main()
