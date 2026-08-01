from pathlib import Path

from bindai_agent import Agent
from bindai_workflow import Workflow
from bindai_workflow.nodes import (
    AgentNode,
    EndNode,
    JoinNode,
    ParallelNode,
    StartNode,
)
from dotenv import load_dotenv

load_dotenv()

BASE = Path(__file__).parent

#
# Load agents
#

agent_a = Agent.from_yaml(
    BASE / "agent_a.yaml",
)

agent_b = Agent.from_yaml(
    BASE / "agent_b.yaml",
)

#
# Register agents
#

workflow = Workflow(
    "parallel-workflow",
)

workflow.agents[agent_a.name] = agent_a
workflow.agents[agent_b.name] = agent_b

#
# Nodes
#

start = StartNode("start")

parallel = ParallelNode("parallel")

branch_a = AgentNode(
    node_id="branch_a",
    agent=agent_a.name,
    input_variable="prompt_a",
    output_variable="result_a",
)

branch_b = AgentNode(
    node_id="branch_b",
    agent=agent_b.name,
    input_variable="prompt_b",
    output_variable="result_b",
)

join = JoinNode(
    "join",
    expected=2,
)

end = EndNode("end")

#
# Register
#

for node in (
    start,
    parallel,
    branch_a,
    branch_b,
    join,
    end,
):
    workflow.add_node(node)

workflow.start_node = start.id

#
# Connections
#

start.next_nodes.append(parallel.id)

parallel.next_nodes.extend(
    [
        branch_a.id,
        branch_b.id,
    ]
)

branch_a.next_nodes.append(join.id)
branch_b.next_nodes.append(join.id)

join.next_nodes.append(end.id)

#
# Input
#

instance = workflow.create_instance()

instance.context.set(
    "prompt_a",
    "Reply with exactly: Branch A completed.",
)

instance.context.set(
    "prompt_b",
    "Reply with exactly: Branch B completed.",
)

#
# Execute
#

result = workflow.executor.execute(
    instance,
)

print()

print("Workflow Result")
print("-" * 40)

print(result.output)

print()

print("Variables")
print(instance.context.variables.as_dict())
