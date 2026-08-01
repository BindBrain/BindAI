from pathlib import Path

from bindai_agent import Agent
from bindai_workflow import WorkflowBuilder
from dotenv import load_dotenv

BASE = Path(__file__).parent

load_dotenv()

agent = Agent.from_yaml(
    BASE / "agent.yaml",
)

workflow = WorkflowBuilder("basic").agent(agent).build()

instance = workflow.create_instance()

instance.context.set(
    "input",
    "Explain what BindAI is in one sentence.",
)

result = workflow.executor.execute(
    instance,
)

print("Workflow Result")
print("-" * 40)

print(result.output)

print("\nVariables")
print(instance.context.variables.as_dict())
