from __future__ import annotations

from bindai_core.context import ExecutionContext

from .result import WorkflowResult
from .workflow import Workflow


class WorkflowExecutor:
    """
    Executes workflow instances.

    The executor itself owns no state.
    All mutable execution state lives inside
    WorkflowContext.
    """

    def execute(
        self,
        workflow: Workflow,
        context: ExecutionContext | None = None,
    ) -> WorkflowResult:

        #
        # Create execution instance
        #

        instance = workflow.create_instance()

        runtime = instance.context

        #
        # Merge external variables
        #

        if context is not None:
            for key, value in context.variables.as_dict().items():
                runtime.set(
                    key,
                    value,
                )

        #
        # Validate workflow
        #

        if workflow.start_node is None:
            return WorkflowResult(
                success=False,
                error="Workflow has no start node.",
            )

        runtime.current_node = workflow.start_node

        #
        # Main execution loop
        #

        while not runtime.completed:
            node = workflow.get(
                runtime.current_node,
            )

            try:
                node.execute(
                    runtime,
                )

            except Exception as ex:
                runtime.completed = True
                runtime.success = False

                runtime.add_error(
                    str(ex),
                )

                return WorkflowResult(
                    success=False,
                    error=str(ex),
                )

            #
            # Workflow finished?
            #

            if runtime.completed:
                break

            #
            # Parallel branch?
            #

            if runtime.parallel_nodes:
                runtime.current_node = runtime.parallel_nodes.pop(0)

                continue

            #
            # Sequential flow
            #

            if not node.next_nodes:
                runtime.completed = True
                runtime.success = True
                break

            runtime.current_node = node.next_nodes[0]

        return WorkflowResult(
            success=runtime.success,
            output=runtime.variables.as_dict(),
        )
