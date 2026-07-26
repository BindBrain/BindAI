from bindai import AgentBuilder
from bindai_core.events import (
    AgentStartedEvent,
    AgentFinishedEvent,
    ToolExecutedEvent,
)
from bindai_core.tool import tool


@tool()
def add(a: int, b: int):
    """Add two integers."""
    return a + b


agent = (
    AgentBuilder()
    .name("Assistant")
    .instructions(
        "Always use the add tool for addition."
    )
    .openai(
        model="gpt-5",
    )
    .tool(add)
    .build()
)


#
# Event Handlers
#

def on_agent_started(event: AgentStartedEvent):
    print("Agent Started")


def on_agent_finished(event: AgentFinishedEvent):
    print("Agent Finished")


def on_tool(event: ToolExecutedEvent):
    print(
        f"Tool Executed: {event.tool_name}"
    )


#
# Subscribe
#

agent.events.subscribe(
    AgentStartedEvent().name,
    on_agent_started,
)

agent.events.subscribe(
    AgentFinishedEvent().name,
    on_agent_finished,
)

agent.events.subscribe(
    ToolExecutedEvent(tool_name="").name,
    on_tool,
)

#
# Manual tool execution
#

print("\nExecuting Tool")

agent.execute_tool(
    "add",
    a=10,
    b=25,
)

#
# Agent execution
#

print("\nRunning Agent")

result = agent.chat(
    "What is 100 + 50?"
)

print(result.response)

#
# Unsubscribe
#

agent.events.unsubscribe(
    ToolExecutedEvent(tool_name="").name,
    on_tool,
)

print("\nTool event unsubscribed.")