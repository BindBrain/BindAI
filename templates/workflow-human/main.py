from pathlib import Path

from bindai_agent import Agent
from bindai_workflow import WorkflowBuilder
from bindai_workflow.nodes import (
    HumanTaskNode,
)
from dotenv import load_dotenv

BASE = Path(__file__).parent

load_dotenv(BASE / ".env")


agent = Agent.from_yaml(
    BASE / "agent.yaml",
)


workflow = (
    WorkflowBuilder("human-workflow")
    .agent(
        agent,
        input_variable="prompt",
        output_variable="result",
    )
    .build()
)


#
# Insert a HumanTaskNode before the agent.
#

human = HumanTaskNode(
    node_id="approval",
)

workflow.add_node(human)

workflow.start_node = human.id

human.next_nodes.append(agent.name)


#
# Create workflow instance
#

instance = workflow.create_instance()

instance.context.set(
    "prompt",
    "Reply with exactly: Human task completed.",
)


#
# Execute
#

result = workflow.executor.execute(
    instance,
)

print()
print("First Execution")
print("----------------------------------------")

if instance.context.waiting:
    print("Workflow paused.")

    print()

    print("Task")

    print(instance.context.task)

else:
    print(result.output)


#
# Simulate user approval
#

print()
print("Resuming workflow...")
print("----------------------------------------")

result = workflow.executor.resume(
    instance,
)

print()
print("Workflow Result")
print("----------------------------------------")

print(result.output["result"].output)

print()

print("Variables")
print(instance.context.variables.as_dict())
