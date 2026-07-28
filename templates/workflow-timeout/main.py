import time

from bindai_workflow import (
    WorkflowBuilder,
    TimeoutPolicy,
)

from bindai_workflow.node import WorkflowNode


class SlowNode(WorkflowNode):
    """
    Sleeps longer than the workflow timeout.
    """

    def __init__(self):

        super().__init__(
            "slow",
        )

    def execute(
        self,
        context,
    ):

        print("Starting long task...")

        time.sleep(3)

        context.set(
            "result",
            "Completed.",
        )


workflow = (
    WorkflowBuilder("timeout-workflow")
    .start(
        SlowNode(),
    )
    .build()
)

instance = workflow.create_instance()

#
# Timeout after 1 second
#

instance.context.timeout_policy = TimeoutPolicy(
    seconds=1,
)

result = workflow.executor.execute(
    instance,
)

print()
print("Workflow Result")
print("----------------------------------------")

if result.success:

    print(result.output)

else:

    print(result.error)

print()

print("Variables")

print(
    instance.context.variables.as_dict(),
)

