from bindai_workflow import Workflow
from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.memory_store import MemoryWorkflowStore
from bindai_workflow.instance import WorkflowInstance
from bindai_workflow.node import WorkflowNode
from bindai_workflow.nodes.condition import ConditionNode


class EndNode(WorkflowNode):

    def execute(self, context):
        context.variables["done"] = self.id
        context.completed = True


def test_condition_true():

    workflow = Workflow("demo")

    condition = ConditionNode(
        "condition",
        lambda ctx: True,
    )

    yes = EndNode("yes")
    no = EndNode("no")

    workflow.add_node(condition)
    workflow.add_node(yes)
    workflow.add_node(no)

    workflow.start_node = condition.id

    condition.when_true(yes)
    condition.when_false(no)

    instance = WorkflowInstance(workflow)

    result = WorkflowExecutor(
        MemoryWorkflowStore(),
    ).execute(instance)

    assert result.success
    assert instance.context.variables["done"] == "yes"


def test_condition_false():

    workflow = Workflow("demo")

    condition = ConditionNode(
        "condition",
        lambda ctx: False,
    )

    yes = EndNode("yes")
    no = EndNode("no")

    workflow.add_node(condition)
    workflow.add_node(yes)
    workflow.add_node(no)

    workflow.start_node = condition.id

    condition.when_true(yes)
    condition.when_false(no)

    instance = WorkflowInstance(workflow)

    result = WorkflowExecutor(
        MemoryWorkflowStore(),
    ).execute(instance)

    assert result.success
    assert instance.context.variables["done"] == "no"