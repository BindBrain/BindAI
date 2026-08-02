"""
16. Parallel Workflow

Demonstrates parallel execution using
BindAI workflow graph nodes.
"""

from bindai_core.executable import Executable, ExecutionResult
from bindai_workflow import Workflow
from bindai_workflow.nodes import (
    EndNode,
    JoinNode,
    ParallelNode,
    RunnableNode,
    StartNode,
)


class ResearchTask(Executable):
    def execute(self, context):

        context.variables["research"] = (
            "AI agents are becoming common in automation, coding, and business workflows."
        )

        return ExecutionResult(
            success=True,
            output=context.variables,
        )


class SummaryTask(Executable):
    def execute(self, context):

        context.variables["summary"] = (
            "Modern AI systems combine models, tools, memory, and orchestration."
        )

        return ExecutionResult(
            success=True,
            output=context.variables,
        )


class MergeTask(Executable):
    def execute(self, context):

        result = {
            "research": context.variables.get("research"),
            "summary": context.variables.get("summary"),
        }

        return ExecutionResult(
            success=True,
            output=result,
        )


workflow = Workflow("parallel-research")


start = StartNode("start")

parallel = ParallelNode("parallel")


research = RunnableNode(
    "research",
    ResearchTask(),
)


summary = RunnableNode(
    "summary",
    SummaryTask(),
)


join = JoinNode(
    "join",
    expected=2,
)


merge = RunnableNode(
    "merge",
    MergeTask(),
)


end = EndNode("end")


# Add nodes

for node in [
    start,
    parallel,
    research,
    summary,
    join,
    merge,
    end,
]:
    workflow.add_node(node)


# Connect graph

start.next_nodes.append(parallel.id)


parallel.next_nodes.extend(
    [
        research.id,
        summary.id,
    ]
)


research.next_nodes.append(join.id)

summary.next_nodes.append(join.id)


join.next_nodes.append(merge.id)


merge.next_nodes.append(end.id)


# Set start

workflow.start_node = start.id


# Execute

result = workflow.run()


print("=" * 60)
print("Parallel Workflow")
print("=" * 60)
print()
print(result)
