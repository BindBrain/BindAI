from datetime import datetime

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

#
# NOTE
#
# WorkflowScheduler currently uses datetime.utcnow()
# internally, so this template intentionally uses the
# same naive datetime until the scheduler is migrated
# to timezone-aware timestamps.
#

schedule = WorkflowSchedule(
    workflow_id=workflow.id,
    next_run=datetime.utcnow(),
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
