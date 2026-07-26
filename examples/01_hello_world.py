from bindai import AgentBuilder

agent = (
    AgentBuilder()
    .name("Assistant")
    .instructions("You are a helpful assistant.")
    .openai(
        model="gpt-5",
    )
    .build()
)

result = agent.chat(
    "What is BindAI?"
)

print(result.response)
