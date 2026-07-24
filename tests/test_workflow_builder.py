from bindai_workflow import WorkflowBuilder
from bindai_workflow.node import WorkflowNode


class Node(WorkflowNode):

    def __init__(self, node_id: str):
        super().__init__(node_id)

    def execute(self, context):
        context.completed = True


def test_builder_start():

    workflow = (
        WorkflowBuilder("Demo")
        .start(Node("start"))
        .build()
    )

    assert workflow.start_node == "start"


def test_builder_then():

    a = Node("a")
    b = Node("b")

    workflow = (
        WorkflowBuilder()
        .start(a)
        .then(b)
        .build()
    )

    assert b.id in a.next_nodes