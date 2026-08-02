"""
20. CLI Assistant

Interactive terminal assistant
powered by BindAI.
"""

from bindai import AgentBuilder


def main():

    agent = AgentBuilder().instructions("You are a helpful terminal assistant.").build()

    print("BindAI CLI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("You: ")

        if message.lower() in {
            "exit",
            "quit",
        }:
            print("Goodbye!")
            break

        result = agent.chat(message)

        print(
            "Assistant:",
            result.output,
        )
        print()


if __name__ == "__main__":
    main()
