from agents.assistant import agent


def main():

    print("BindAI Project")

    while True:

        message = input("You: ")

        if message.lower() == "exit":
            break

        response = agent.run(message)

        print(f"Assistant: {response}")


if __name__ == "__main__":
    main()