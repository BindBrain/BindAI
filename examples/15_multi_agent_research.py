"""
15. Multi-Agent Research

Demonstrates multiple agents collaborating
to research, analyze and summarize a topic.
"""

from bindai import (
    AgentBuilder,
    GroupBuilder,
    Task,
)

print("=" * 60)
print("Multi-Agent Research")
print("=" * 60)


#
# Research Agent
#

researcher = (
    AgentBuilder()
    .name("Researcher")
    .instructions(
        """
        You are an expert researcher.

        Collect accurate facts,
        technologies,
        companies,
        and trends.
        """
    )
    .openai(
        model="gpt-5",
    )
    .build()
)


#
# Analyst Agent
#

analyst = (
    AgentBuilder()
    .name("Analyst")
    .instructions(
        """
        Analyze research results.

        Identify important patterns,
        strengths,
        weaknesses,
        opportunities,
        and future trends.
        """
    )
    .openai(
        model="gpt-5",
    )
    .build()
)


#
# Writer Agent
#

writer = (
    AgentBuilder()
    .name("Writer")
    .instructions(
        """
        Produce a concise,
        well-structured report
        using the provided context.
        """
    )
    .openai(
        model="gpt-5",
    )
    .build()
)


#
# Tasks
#

research = Task(
    description="""
Research the future of AI agent frameworks.

Include:

- current trends
- major frameworks
- enterprise adoption
- challenges
- future direction
""",
    agent=researcher,
)

analysis = Task(
    description="""
Analyze the research.

Identify the most important insights.
""",
    agent=analyst,
).context_from(research)

report = Task(
    description="""
Write a final report.

Keep it concise and professional.
""",
    agent=writer,
).context_from(
    research,
    analysis,
)


#
# Group
#

group = (
    GroupBuilder()
    .name("AI Research Team")
    .agent(researcher)
    .agent(analyst)
    .agent(writer)
    .task(research)
    .task(analysis)
    .task(report)
    .build()
)


#
# Execute
#

result = group.run()

print("\nSuccess:")
print(result.success)

print("\nOutput:\n")

print(result.output)
