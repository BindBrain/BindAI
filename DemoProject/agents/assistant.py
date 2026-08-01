from bindai_agent import AgentBuilder

agent = (
    AgentBuilder()
    .from_project()
    .instructions(
        """
        You are a helpful AI assistant.
        """
    )
    .build()
)
