from dotenv import load_dotenv

load_dotenv()

from agents.assistant import agent  # noqa: E402


def main():
    print("BindAI Project")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            break

        response = agent.run(message)

        print(f"Assistant: {response.output}")


if __name__ == "__main__":
    main()
