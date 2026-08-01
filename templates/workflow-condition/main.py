from pathlib import Path

from bindai import Agent
from bindai_agent import AgentRegistry
from bindai_workflow import Workflow
from bindai_workflow.nodes import (
    AgentNode,
    ConditionNode,
    EndNode,
    StartNode,
)
from dotenv import load_dotenv

load_dotenv()

BASE = Path(__file__).parent

#
# Load agent
#

agent = Agent.from_yaml(
    BASE / "agent.yaml",
)

#
# Register agent
#

AgentRegistry.register(
    agent,
)

#
# Build workflow
#

workflow = Workflow(
    "condition-demo",
)

#
# Nodes
#

start = StartNode(
    "start",
)

condition = ConditionNode(
    "condition",
    lambda ctx: ctx.get(
        "approved",
        False,
    ),
)

approved = AgentNode(
    "approved",
    agent=agent.name,
    input_variable="approved_prompt",
    output_variable="approved_result",
)

rejected = AgentNode(
    "rejected",
    agent=agent.name,
    input_variable="rejected_prompt",
    output_variable="rejected_result",
)

end = EndNode(
    "end",
)

#
# Add nodes
#

workflow.add_node(start)
workflow.add_node(condition)
workflow.add_node(approved)
workflow.add_node(rejected)
workflow.add_node(end)

workflow.start_node = start.id

#
# Connections
#

start.next_nodes.append(
    condition.id,
)

condition.true_node = approved.id
condition.false_node = rejected.id

approved.next_nodes.append(
    end.id,
)

rejected.next_nodes.append(
    end.id,
)

#
# Create instance
#

instance = workflow.create_instance()

#
# Toggle this between True / False
#

instance.context.set(
    "approved",
    True,
)

instance.context.set(
    "approved_prompt",
    "Reply with exactly: Request approved.",
)

instance.context.set(
    "rejected_prompt",
    "Reply with exactly: Request rejected.",
)

#
# Execute workflow
#

workflow.executor.execute(
    instance,
)

#
# Display result
#

variables = instance.context.variables.as_dict()

print("Workflow Result")
print("-" * 40)

if "approved_result" in variables:
    print(
        variables["approved_result"].output,
    )

elif "rejected_result" in variables:
    print(
        variables["rejected_result"].output,
    )

print()

print("Variables")

print(
    variables,
)
