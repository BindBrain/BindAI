from bindai import (
    AgentBuilder,
    GroupBuilder,
    Task,
)

#
# Agents
#

researcher = (
    AgentBuilder()
    .name("Researcher")
    .instructions("Research the requested topic.")
    .openai(
        model="gpt-5",
    )
    .build()
)

writer = (
    AgentBuilder()
    .name("Writer")
    .instructions("Write a concise summary.")
    .openai(
        model="gpt-5",
    )
    .build()
)


#
# Tasks
#

research_task = Task(
    description="Research what BindAI is.",
    agent=researcher,
)

summary_task = Task(
    description="Summarize the research in one paragraph.",
    agent=writer,
).context_from(
    research_task,
)


#
# Group
#

group = (
    GroupBuilder()
    .name("Research Group")
    .agent(researcher)
    .agent(writer)
    .task(research_task)
    .task(summary_task)
    .build()
)


#
# Execute
#

result = group.run()


print("Success:", result.success)

print()

print("Output:")

print(result.output)
