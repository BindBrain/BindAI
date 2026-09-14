from datetime import UTC, datetime

from bindai_workflow import (
    WorkflowBuilder,
    WorkflowSchedule,
    WorkflowScheduler,
)
from bindai_workflow.node import WorkflowNode


class PrintNode(WorkflowNode):
    def __init__(self):

        super().__init__(
            "print",
        )

    def execute(
        self,
        context,
    ):

        print("Scheduled workflow executed.")

        context.set(
            "result",
            "Workflow executed by scheduler.",
        )


#
# Build workflow
#

workflow = (
    WorkflowBuilder(
        "scheduled-workflow",
    )
    .start(
        PrintNode(),
    )
    .build()
)

#
# Create scheduler
#

scheduler = WorkflowScheduler()

schedule = WorkflowSchedule(
    workflow_id=workflow.id,
    next_run=datetime.now(UTC),
    interval_seconds=60,
)

scheduler.add(
    schedule,
)

print("Checking schedules...")
print("----------------------------------------")

for item in scheduler.due():
    print(f"Running workflow: {item.workflow_id}")

    instance = workflow.create_instance()

    result = workflow.executor.execute(
        instance,
    )

    print()

    print("Workflow Result")
    print("----------------------------------------")

    if result.success:
        print(
            result.output["result"],
        )
    else:
        print(
            result.error,
        )

    print()

    print("Variables")

    print(
        instance.context.variables.as_dict(),
    )

    scheduler.reschedule(
        item,
    )

print()

print("Next run")

print(
    schedule.next_run,
)