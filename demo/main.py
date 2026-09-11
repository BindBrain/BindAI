from bindai import Agent


agent = (
    Agent.builder()
    .name("assistant")
    .instructions("You are a helpful assistant.")
    .build()
)

response = agent.run("Hello!")

print(response.output)