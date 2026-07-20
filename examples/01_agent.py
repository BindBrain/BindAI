from bindai import AgentBuilder


agent = (
    AgentBuilder()
    .name("Assistant")
    .instructions(
        "You are a helpful assistant."
    )
    .openai(
        model="gpt-4.1-mini",
    )
    .build()
)

result = agent.chat(
    "Explain what OpenAI does."
)

print(
    result.output,
)