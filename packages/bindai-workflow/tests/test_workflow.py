from bindai_tool import tool
from bindai_workflow import WorkflowBuilder
from bindai_workflow.node import WorkflowNode
from bindai_workflow.nodes.end import EndNode
from bindai_workflow.nodes.human import HumanTaskNode
from bindai_workflow.nodes.join import JoinNode
from bindai_workflow.nodes.parallel import ParallelNode
from bindai_workflow.nodes.subworkflow import SubWorkflowNode


class RecordingNode(WorkflowNode):
    def __init__(self, node_id, executed):
        super().__init__(node_id)
        self.executed = executed

    def execute(self, context):
        self.executed.append(self.id)
        return context


@tool
def echo(text: str) -> str:
    return text


def test_workflow_executes_tool_and_stores_result():
    workflow = (
        WorkflowBuilder("tool-workflow")
        .start_node()
        .tool(
            echo,
            output_variable="result",
        )
        .end_node()
        .build()
    )

    instance = workflow.create_instance()
    instance.context.set("text", "hello")

    result = workflow.executor.execute(instance)

    assert result.success is True
    assert result.output.get("result").value == "hello"


def test_builder_creates_human_task_node():
    workflow = (
        WorkflowBuilder("human-workflow")
        .start_node()
        .human_task(
            assignee="reviewer@example.com",
            form="review",
            node_id="review",
        )
        .end_node()
        .build()
    )

    node = workflow.get("review")

    assert isinstance(node, HumanTaskNode)
    assert node.assignee == "reviewer@example.com"
    assert node.form == "review"
    assert node.next_nodes == ["end"]


def test_builder_creates_subworkflow_node():
    workflow = (
        WorkflowBuilder("parent")
        .start_node()
        .subworkflow(
            "child-workflow",
            node_id="child",
        )
        .end_node()
        .build()
    )

    node = workflow.get("child")

    assert isinstance(node, SubWorkflowNode)
    assert node.workflow_id == "child-workflow"
    assert node.next_nodes == ["end"]


def test_subworkflow_executes_child_and_returns_variables():
    class Project:
        def workflow(self, workflow_id):
            if workflow_id == "child":
                return child

            return None

    child = WorkflowBuilder("child").start_node().build()

    parent = WorkflowBuilder("parent").start_node().subworkflow("child").end_node().build()

    instance = parent.create_instance()
    instance.project = Project()
    instance.context.set("input", "hello")

    result = parent.executor.execute(instance)

    assert result.success is True
    assert result.output.get("input") == "hello"


def test_condition_executes_true_branch():
    executed = []

    true_node = RecordingNode("approved", executed)
    false_node = RecordingNode("rejected", executed)

    workflow = (
        WorkflowBuilder("condition-workflow")
        .start_node()
        .condition(
            lambda context: context.get("approved"),
            when_true=true_node,
            when_false=false_node,
        )
        .build()
    )

    instance = workflow.create_instance()
    instance.context.set("approved", True)

    result = workflow.executor.execute(instance)

    assert result.success is True
    assert executed == ["approved"]


def test_condition_executes_false_branch():
    executed = []

    true_node = RecordingNode("approved", executed)
    false_node = RecordingNode("rejected", executed)

    workflow = (
        WorkflowBuilder("condition-workflow")
        .start_node()
        .condition(
            lambda context: context.get("approved"),
            when_true=true_node,
            when_false=false_node,
        )
        .build()
    )

    instance = workflow.create_instance()
    instance.context.set("approved", False)

    result = workflow.executor.execute(instance)

    assert result.success is True
    assert executed == ["rejected"]


def test_builder_creates_parallel_branches_and_join():
    executed = []

    branch_a = RecordingNode("branch_a", executed)
    branch_b = RecordingNode("branch_b", executed)

    workflow = (
        WorkflowBuilder("parallel-workflow")
        .start_node()
        .parallel(
            branch_a,
            branch_b,
        )
        .join()
        .end_node()
        .build()
    )

    parallel = workflow.get("parallel_1")
    join = workflow.get("join_4")

    assert isinstance(parallel, ParallelNode)
    assert isinstance(join, JoinNode)
    assert parallel.next_nodes == ["branch_a", "branch_b"]
    assert branch_a.next_nodes == ["join_4"]
    assert branch_b.next_nodes == ["join_4"]
    assert join.next_nodes == ["end"]


def test_builder_creates_executable_loop():
    class IncrementNode(WorkflowNode):
        def execute(self, context):
            context.set(
                "count",
                context.get("count") + 1,
            )
            return context

    body = IncrementNode("increment")
    exit_node = EndNode("exit")

    workflow = (
        WorkflowBuilder("loop-workflow")
        .start_node()
        .loop(
            lambda context: context.get("count") < 3,
            body=body,
            exit=exit_node,
        )
        .build()
    )

    instance = workflow.create_instance()
    instance.context.set("count", 0)

    result = workflow.executor.execute(instance)

    assert result.success is True
    assert result.output.get("count") == 3
    assert instance.context.completed is True


def test_builder_human_task_pauses_and_resumes():
    executed = []

    after = RecordingNode("after", executed)

    workflow = (
        WorkflowBuilder("human-workflow")
        .start_node()
        .human_task(
            assignee="reviewer@example.com",
        )
        .then(after)
        .end_node()
        .build()
    )

    instance = workflow.create_instance()

    result = workflow.executor.execute(instance)

    assert result.success is True
    assert instance.context.waiting is True
    assert instance.context.task is not None
    assert instance.context.task.assignee == "reviewer@example.com"
    assert executed == []

    instance.context.task.approve()

    result = workflow.executor.resume(instance)

    assert result.success is True
    assert instance.context.waiting is False
    assert instance.context.task.completed is True
    assert instance.context.task.result == "approved"
    assert executed == ["after"]
