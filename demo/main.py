from bindai import Agent


agent = Agent(
    instructions="You are a helpful assistant.",
)

response = agent.run("Hello!")

print(response)
