from bindai_workflow import (
    RetryPolicy,
    WorkflowBuilder,
)
from bindai_workflow.node import WorkflowNode


class RetryNode(WorkflowNode):
    """
    Fails twice before succeeding.
    """

    def __init__(self):

        super().__init__("retry")

        self.calls = 0

    def execute(
        self,
        context,
    ):

        self.calls += 1

        print(f"Attempt {self.calls}")

        if self.calls < 3:
            raise RuntimeError("Temporary failure.")

        context.set(
            "result",
            "Succeeded after retries.",
        )


workflow = (
    WorkflowBuilder("retry-workflow")
    .start(
        RetryNode(),
    )
    .build()
)

#
# Enable retry policy
#

instance = workflow.create_instance()

instance.context.retry_policy = RetryPolicy(
    max_attempts=3,
)

result = workflow.executor.execute(
    instance,
)

print()
print("Workflow Result")
print("----------------------------------------")

if result.success:
    print(result.output["result"])
else:
    print(result.error)

print()
print("Variables")
print(instance.context.variables.as_dict())
