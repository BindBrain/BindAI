from __future__ import annotations

from datetime import datetime, timedelta

from .events import WorkflowEvent
from .history import WorkflowHistory
from .history_store import MemoryHistoryStore
from .instance import WorkflowInstance
from .result import WorkflowResult


class WorkflowExecutor:
    """
    Executes workflow instances.
    """

    def __init__(
        self,
        store,
        history_store=None,
    ):

        self.store = store

        self.history_store = history_store or MemoryHistoryStore()

    #
    # Public API
    #

    def execute(
        self,
        instance: WorkflowInstance,
    ) -> WorkflowResult:

        workflow = instance.workflow

        context = instance.context

        #
        # Persist immediately
        #

        self.store.save(
            instance,
        )

        #
        # Workflow started
        #

        context.events.append(
            WorkflowEvent(
                type="workflow.started",
                timestamp=datetime.utcnow(),
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                instance_id=instance.id,
            )
        )

        #
        # Validate workflow
        #

        if workflow.start_node is None:
            return self._failure(
                instance,
                "Workflow has no start node.",
            )

        #
        # Start execution
        #

        context.current_node = workflow.start_node

        return self._run(
            instance,
        )

    def resume(
        self,
        instance: WorkflowInstance,
    ) -> WorkflowResult:
        """
        Resume a paused workflow.
        """

        context = instance.context

        if not context.waiting:
            raise RuntimeError(
                "Workflow is not waiting.",
            )

        context.waiting = False

        return self._run(
            instance,
        )

    #
    # Main execution loop
    #

    def _run(
        self,
        instance: WorkflowInstance,
    ) -> WorkflowResult:

        workflow = instance.workflow

        context = instance.context

        while not context.completed:
            #
            # Timeout
            #

            policy = context.timeout_policy

            if policy is not None:
                elapsed = datetime.utcnow() - context.started_at

                if elapsed > timedelta(
                    seconds=policy.seconds,
                ):
                    return self._failure(
                        instance,
                        "Workflow timeout.",
                    )

            #
            # Current node
            #

            node = workflow.get(
                context.current_node,
            )

            #
            # Reset retry counter
            #

            context.retry_attempt = 0

            #
            # Node started
            #

            context.events.append(
                WorkflowEvent(
                    type="node.started",
                    timestamp=datetime.utcnow(),
                    workflow_id=workflow.id,
                    workflow_version=workflow.version,
                    instance_id=instance.id,
                    node_id=node.id,
                )
            )

            #
            # Execute node
            #

            result = self._execute_node(
                instance,
                node,
            )

            if result is not None:
                return result

            #
            # Execute sub workflow
            #

            if context.subworkflow is not None:
                child_workflow = instance.project.workflow(
                    context.subworkflow,
                )

                child = child_workflow.create_instance()

                child.project = instance.project

                child.context.variables.update(
                    context.variables,
                )

                child_result = self.execute(
                    child,
                )

                if not child_result.success:
                    return child_result

                context.variables.update(
                    child.context.variables,
                )

                context.subworkflow = None

            #
            # Persist checkpoint
            #

            self.store.save(
                instance,
            )

            #
            # Waiting for external action?
            #

            if context.waiting:
                return WorkflowResult(
                    success=True,
                    output=context.variables,
                )

            #
            # Node completed
            #

            context.events.append(
                WorkflowEvent(
                    type="node.completed",
                    timestamp=datetime.utcnow(),
                    workflow_id=workflow.id,
                    workflow_version=workflow.version,
                    instance_id=instance.id,
                    node_id=node.id,
                )
            )

            #
            # Workflow completed?
            #

            if context.completed:
                break

            #
            # Parallel queue
            #

            if context.parallel_nodes:
                context.current_node = context.parallel_nodes.pop(0)

                continue

            #
            # Sequential execution
            #

            if context.current_node == node.id:
                if not node.next_nodes:
                    return self._failure(
                        instance,
                        (f"Node '{node.id}' has no outgoing connection."),
                    )

                context.current_node = node.next_nodes[0]

        #
        # Workflow completed
        #

        context.finished_at = datetime.utcnow()

        context.events.append(
            WorkflowEvent(
                type="workflow.completed",
                timestamp=context.finished_at,
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                instance_id=instance.id,
            )
        )

        #
        # Persist final state
        #

        self.store.save(
            instance,
        )

        #
        # Save execution history
        #

        self.history_store.add(
            WorkflowHistory(
                instance_id=instance.id,
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                started_at=context.started_at,
                finished_at=context.finished_at,
                success=True,
            )
        )

        return WorkflowResult(
            success=True,
            output=context.variables,
        )

    #
    # Execute one node
    #

    def _execute_node(
        self,
        instance: WorkflowInstance,
        node,
    ) -> WorkflowResult | None:

        context = instance.context

        while True:
            try:
                #
                # Execute the node
                #

                node.execute(
                    context,
                )

                #
                # Reset retry counter after success
                #

                context.retry_attempt = 0

                return None

            except Exception as ex:
                #
                # Retry policy
                #

                policy = context.retry_policy

                if policy is None:
                    return self._failure(
                        instance,
                        str(ex),
                    )

                #
                # Increment retry count
                #

                context.retry_attempt += 1

                #
                # Retry exhausted
                #

                if context.retry_attempt >= policy.max_attempts:
                    return self._failure(
                        instance,
                        str(ex),
                    )

                #
                # Future:
                #
                # sleep(policy.delay_seconds)
                # exponential backoff
                # retry event
                #
                # Loop continues automatically
                #

    #
    # Failure
    #

    def _failure(
        self,
        instance: WorkflowInstance,
        error: str,
    ) -> WorkflowResult:

        context = instance.context

        workflow = instance.workflow

        #
        # Execute compensations
        #

        while context.compensations:
            compensation = context.compensations.pop()

            try:
                compensation(
                    context,
                )

            except Exception:
                #
                # Ignore compensation failures.
                #
                # Never mask the original error.
                #

                pass

        #
        # Record error
        #

        context.errors.append(
            error,
        )

        context.completed = True

        context.finished_at = datetime.utcnow()

        #
        # Workflow failed event
        #

        context.events.append(
            WorkflowEvent(
                type="workflow.failed",
                timestamp=context.finished_at,
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                instance_id=instance.id,
            )
        )

        #
        # Persist state
        #

        self.store.save(
            instance,
        )

        #
        # Store execution history
        #

        self.history_store.add(
            WorkflowHistory(
                instance_id=instance.id,
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                started_at=context.started_at,
                finished_at=context.finished_at,
                success=False,
                error=error,
            )
        )

        return WorkflowResult(
            success=False,
            error=error,
        )
