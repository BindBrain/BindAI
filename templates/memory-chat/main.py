from bindai import Agent

agent = Agent.from_yaml("agent.yaml")

while True:
    message = input("You: ")

    if message.lower() in {"quit", "exit"}:
        break

    result = agent.chat(message)

    print(result.output)
