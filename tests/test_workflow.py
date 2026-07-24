from bindai_workflow import Workflow
from bindai_workflow.node import WorkflowNode
from bindai_workflow.context import WorkflowContext


class DummyNode(WorkflowNode):
    def execute(self, context):
        context.variables["executed"] = True
        context.completed = True


def test_create_workflow():

    workflow = Workflow("demo")

    assert workflow.name == "demo"
    assert workflow.start_node is None
    assert workflow.nodes == {}


def test_add_node_sets_start_node():

    workflow = Workflow()

    node = DummyNode("start")

    workflow.add_node(node)

    assert workflow.start_node == "start"
    assert workflow.get("start") is node


def test_create_instance():

    workflow = Workflow()

    workflow.add_node(DummyNode("start"))

    instance = workflow.create_instance()

    assert instance.workflow is workflow


def test_execute_single_node():

    workflow = Workflow()

    workflow.add_node(DummyNode("start"))

    instance = workflow.create_instance()

    result = workflow.executor.execute(instance)

    assert result.success
    assert instance.context.variables["executed"] is True