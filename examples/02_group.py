from bindai import (
    AgentBuilder,
    GroupBuilder,
    Task,
)


researcher = (
    AgentBuilder()
    .name("Researcher")
    .instructions(
        "Research companies."
    )
    .openai(
        model="gpt-4.1-mini",
    )
    .build()
)

writer = (
    AgentBuilder()
    .name("Writer")
    .instructions(
        "Write executive reports."
    )
    .openai(
        model="gpt-4.1-mini",
    )
    .build()
)


research = Task(
    description="Research OpenAI.",
    agent=researcher,
)

report = (
    Task(
        description="Write an executive summary.",
        agent=writer,
    )
    .context_from(
        research,
    )
)


group = (
    GroupBuilder()
    .name("Marketing")
    .agent(researcher)
    .agent(writer)
    .task(research)
    .task(report)
    .build()
)


result = group.run()

print(
    result.output,
)