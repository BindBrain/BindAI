from bindai_agent import AgentBuilder

agent = (
    AgentBuilder()
    .name("Research")
    .instructions("Research assistant.")
    .model("openai:gpt-4.1-mini")
    .build()
)
