from bindai_core.workflow import (
    Workflow,
    WorkflowNode,
    WorkflowExecutor,
)
from bindai_core.context import ExecutionContext


class Step1:
    def execute(self, context):
        print("Step 1")


class Step2:
    def execute(self, context):
        print("Step 2")


workflow = Workflow("Demo Workflow")

workflow.add_node(
    WorkflowNode(
        id="step1",
        executable=Step1(),
    )
)

workflow.add_node(
    WorkflowNode(
        id="step2",
        executable=Step2(),
    )
)

executor = WorkflowExecutor()

result = executor.execute(
    workflow,
    ExecutionContext(),
)

print(result.success)