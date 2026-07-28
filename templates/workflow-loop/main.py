from pathlib import Path

from bindai_agent import Agent, AgentRegistry

from bindai_workflow import WorkflowBuilder
from bindai_workflow.nodes import (
    LoopNode,
    AgentNode,
    EndNode,
)

BASE = Path(__file__).parent

#
# Load agent
#

agent = Agent.from_yaml(
    BASE / "agent.yaml",
)

AgentRegistry.register(
    agent,
)

#
# Loop condition
#

def should_continue(ctx):

    return ctx.get(
        "counter",
        0,
    ) < 3


builder = WorkflowBuilder(
    "workflow-loop",
)

loop = LoopNode(
    node_id="loop",
    predicate=should_continue,
)

worker = AgentNode(
    node_id="worker",
    agent="loop-agent",
    input_variable="prompt",
    output_variable="result",
)

end = EndNode(
    "end",
)

builder.start(loop)

builder.add(worker)
builder.add(end)

#
# next_nodes
#
# [0] -> loop body
# [1] -> exit
#

loop.next_nodes.append(
    worker.id,
)

loop.next_nodes.append(
    end.id,
)

#
# After executing the worker,
# return to the loop.
#

worker.next_nodes.append(
    loop.id,
)

workflow = builder.build()

instance = workflow.create_instance()

instance.context.set(
    "counter",
    0,
)

instance.context.set(
    "prompt",
    "Reply with exactly: Loop executed.",
)

#
# Increment counter every pass.
#

original_execute = worker.execute


def execute(context):

    original_execute(context)

    context.set(
        "counter",
        context.get(
            "counter",
        )
        + 1,
    )

    return context


worker.execute = execute

result = workflow.executor.execute(
    instance,
)

print()

print("Workflow Result")
print("----------------------------------------")

agent_result = result.output.get(
    "result",
)

if agent_result:
    print(
        agent_result.output,
    )

print()

print("Variables")
print(
    instance.context.variables.as_dict(),
)