"""
08_workflow.py

Learn how to:

- Create a workflow
- Create custom workflow nodes
- Connect workflow nodes
- Execute a workflow
"""

from bindai_core.context import ExecutionContext
from bindai_workflow import Workflow
from bindai_workflow.node import WorkflowNode

# ==========================================================
# Workflow Nodes
# ==========================================================


class Step1Node(WorkflowNode):
    def __init__(self):
        super().__init__("step1", "Step 1")

    def execute(self, context):
        print("Step 1")

        context.variables.set(
            "message",
            "Hello from Step 1",
        )

        return context


class Step2Node(WorkflowNode):
    def __init__(self):
        super().__init__("step2", "Step 2")

    def execute(self, context):
        print("Step 2")

        print(
            "Message:",
            context.variables.get("message"),
        )

        return context


# ==========================================================
# Build Workflow
# ==========================================================

workflow = Workflow("Demo Workflow")

step1 = Step1Node()
step2 = Step2Node()

step1.next_nodes.append("step2")

workflow.add_node(step1)
workflow.add_node(step2)


# ==========================================================
# Execute
# ==========================================================

print("=" * 60)
print("Workflow")
print("=" * 60)

result = workflow.run(
    ExecutionContext(),
)

print("\nWorkflow Success:", result.success)
