from bindai_workflow import Workflow
from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.instance import WorkflowInstance
from bindai_workflow.memory_store import MemoryWorkflowStore
from bindai_workflow.node import WorkflowNode
from bindai_workflow.nodes.parallel import ParallelNode


class EndNode(WorkflowNode):
    def execute(
        self,
        context,
    ):

        visited = context.variables.get(
            "visited",
            [],
        )

        visited.append(
            self.id,
        )

        context.variables["visited"] = visited

        if len(visited) == 2:
            context.completed = True


def test_parallel():

    workflow = Workflow("parallel")

    start = ParallelNode("parallel")

    a = EndNode("a")
    b = EndNode("b")

    workflow.add_node(start)
    workflow.add_node(a)
    workflow.add_node(b)

    workflow.start_node = start.id

    start.next_nodes.append(a.id)
    start.next_nodes.append(b.id)

    instance = WorkflowInstance(workflow)

    result = WorkflowExecutor(
        MemoryWorkflowStore(),
    ).execute(instance)

    assert result.success

    assert set(
        instance.context.variables["visited"],
    ) == {
        "a",
        "b",
    }
