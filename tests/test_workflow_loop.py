from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.instance import WorkflowInstance
from bindai_workflow.memory_store import MemoryWorkflowStore
from bindai_workflow.node import WorkflowNode
from bindai_workflow.nodes.loop import LoopNode
from bindai_workflow.workflow import Workflow


class IncrementNode(WorkflowNode):

    def execute(
        self,
        context,
    ):

        counter = context.variables.get(
            "counter",
            0,
        )

        counter += 1

        context.variables["counter"] = counter


class EndNode(WorkflowNode):

    def execute(
        self,
        context,
    ):

        context.variables["done"] = True


def test_loop():

    workflow = Workflow("loop")

    loop = LoopNode(
        "loop",
        lambda ctx: ctx.variables.get("counter", 0) < 5,
    )

    body = IncrementNode("body")

    end = EndNode("end")

    workflow.add_node(loop)
    workflow.add_node(body)
    workflow.add_node(end)

    workflow.start_node = loop.id

    #
    # next_nodes:
    #
    # [0] loop body
    # [1] exit
    #

    loop.next_nodes.append(body.id)
    loop.next_nodes.append(end.id)

    body.next_nodes.append(loop.id)

    instance = WorkflowInstance(workflow)

    result = WorkflowExecutor(
        MemoryWorkflowStore(),
    ).execute(instance)

    assert result.success

    assert instance.context.variables["counter"] == 5

    assert instance.context.variables["done"] is True