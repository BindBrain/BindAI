"""
18. Retry & Timeout

Demonstrates workflow reliability features:
- retrying failed tasks
- protecting execution with timeout limits
"""

import time

from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable
from bindai_core.executable.result import ExecutionResult
from bindai_workflow import (
    RetryPolicy,
    TimeoutPolicy,
    WorkflowBuilder,
)
from bindai_workflow.nodes.runnable import RunnableNode

# ============================================================
# Helper executable wrapper
# ============================================================


class FunctionExecutable(Executable):
    def __init__(self, fn):
        self.fn = fn

    def execute(
        self,
        context: ExecutionContext,
    ):

        result = self.fn(context.variables)

        return ExecutionResult(
            success=True,
            output=result,
        )


# ============================================================
# Retry example
# ============================================================

attempts = 0


def unstable_task(context):

    global attempts

    attempts += 1

    print(f"Running attempt {attempts}")

    if attempts < 3:
        raise RuntimeError("Temporary failure")

    return {"message": ("Task completed successfully after retries")}


# ============================================================
# Timeout example
# ============================================================


def slow_task(context):

    print("Starting slow task...")

    time.sleep(10)

    return {"message": "Finished"}


# ============================================================
# Build workflow
# ============================================================

workflow = (
    WorkflowBuilder("retry-timeout-example")
    .start_node()
    .then(
        RunnableNode(
            "unstable_task",
            FunctionExecutable(unstable_task),
        )
    )
    .then(
        RunnableNode(
            "slow_task",
            FunctionExecutable(slow_task),
        )
    )
    .end_node()
    .build()
)


# ============================================================
# Configure policies
# ============================================================

instance = workflow.create_instance()


# Retry failed nodes
instance.context.retry_policy = RetryPolicy(
    max_attempts=3,
    delay_seconds=1,
)


# Timeout entire workflow
instance.context.timeout_policy = TimeoutPolicy(
    seconds=5,
)


# ============================================================
# Execute
# ============================================================

result = workflow.executor.execute(instance)


print()
print("=" * 60)
print("RESULT")
print("=" * 60)
print(result)
