from bindai_workflow.executor import WorkflowExecutor
from bindai_workflow.instance import WorkflowInstance
from bindai_workflow.memory_store import MemoryWorkflowStore
from bindai_workflow.node import WorkflowNode
from bindai_workflow.nodes.join import JoinNode
from bindai_workflow.nodes.parallel import ParallelNode
from bindai_workflow.workflow import Workflow


class EndNode(WorkflowNode):
    def execute(
        self,
        context,
    ):

        visited = context.variables.get(
            "visited",
            [],
        )

        visited.append(self.id)

        context.variables["visited"] = visited


def test_join():

    workflow = Workflow("join")

    start = ParallelNode("parallel")

    a = EndNode("a")
    b = EndNode("b")

    join = JoinNode(
        "join",
        expected=2,
    )

    end = EndNode("end")

    workflow.add_node(start)
    workflow.add_node(a)
    workflow.add_node(b)
    workflow.add_node(join)
    workflow.add_node(end)

    workflow.start_node = start.id

    start.next_nodes.extend(
        [
            a.id,
            b.id,
        ]
    )

    a.next_nodes.append(
        join.id,
    )

    b.next_nodes.append(
        join.id,
    )

    join.next_nodes.append(
        end.id,
    )

    instance = WorkflowInstance(
        workflow,
    )

    result = WorkflowExecutor(
        MemoryWorkflowStore(),
    ).execute(
        instance,
    )

    assert result.success

    assert set(
        instance.context.variables["visited"],
    ) == {
        "a",
        "b",
        "end",
    }
