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

print("Streaming:\n")

for chunk in agent.stream(
    "Explain BindAI in one paragraph."
):
    print(chunk.delta, end="", flush=True)

print("\n\nFinished.")