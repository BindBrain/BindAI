from bindai import AgentBuilder

agent = (
    AgentBuilder()
    .name("BindAI Assistant")
    .instructions(
        """
        You are the official BindAI assistant.

        BindAI is an open-source Python framework
        for building production AI applications.

        It provides:

        - AI agents
        - workflows
        - tools
        - memory systems
        - knowledge retrieval
        - multi-agent systems
        - provider integrations

        Answer questions about this framework.
        """
    )
    .openai(
        model="gpt-5",
    )
    .build()
)


result = agent.chat("Introduce BindAI and explain its main capabilities.")


print(result.output)
