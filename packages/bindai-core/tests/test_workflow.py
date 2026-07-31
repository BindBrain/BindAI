from bindai_core.workflow import (
    Workflow,
    WorkflowExecutor,
    WorkflowNode,
)


class HelloNode(WorkflowNode):
    def execute(self, context):

        context.set(
            "message",
            "Hello BindAI",
        )

        context.completed = True
        context.success = True


def test_workflow_runs():

    workflow = Workflow("demo")

    workflow.add_node(HelloNode("start"))

    executor = WorkflowExecutor()

    result = executor.execute(workflow)

    assert result.success

    assert result.output["message"] == "Hello BindAI"
