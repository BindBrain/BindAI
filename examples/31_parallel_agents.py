"""31. Parallel Agents

Run independent agents concurrently inside an agent group.
"""

from bindai import AgentBuilder, GroupBuilder, Task
from bindai_group.processes import ParallelProcess

researcher = (
AgentBuilder()
.name("Researcher")
.openai(model="gpt-5")
.build()
)

analyst = (
AgentBuilder()
.name("Analyst")
.openai(model="gpt-5")
.build()
)

research_task = Task(
description=(
"Research the main benefits and challenges of "
"using AI agents in software development."
),
agent=researcher,
expected_output="A concise research summary.",
)

analysis_task = Task(
description=(
"Analyze the main technical considerations when "
"deploying AI agents in production."
),
agent=analyst,
expected_output="A concise technical analysis.",
)

group = (
GroupBuilder()
.name("Parallel Agents")
.agent(researcher)
.agent(analyst)
.task(research_task)
.task(analysis_task)
.process(ParallelProcess())
.build()
)

result = group.run()

print("Success:", result.success)
print()
print(result.output)
