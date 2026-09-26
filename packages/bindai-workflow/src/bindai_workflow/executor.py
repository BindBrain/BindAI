from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from .events import WorkflowEvent
from .history import WorkflowHistory
from .history_store import MemoryHistoryStore
from .instance import WorkflowInstance
from .result import WorkflowResult

if TYPE_CHECKING:
    from .history_store_protocol import WorkflowHistoryStore
    from .node import WorkflowNode
    from .store import WorkflowStore


class WorkflowExecutor:
    """
    Executes workflow instances.

    The workflow executor remains the source of truth for workflow
    execution and lifecycle events.

    An optional event_handler can be supplied by the runtime layer to
    observe workflow lifecycle events without introducing a second
    execution engine or event system.
    """

    def __init__(
        self,
        store: WorkflowStore,
        history_store: WorkflowHistoryStore | None = None,
        event_handler=None,
    ):
        self.store = store
        self.history_store = history_store or MemoryHistoryStore()
        self.event_handler = event_handler

    #
    # Event handling
    #

    def _emit_event(
        self,
        event: WorkflowEvent,
    ) -> None:
        """
        Notify an optional external event handler.

        WorkflowContext.events remains the workflow-local event history.
        The external handler allows the runtime layer to bridge these
        events into the BindAI runtime EventBus.
        """

        if self.event_handler is not None:
            self.event_handler(
                event,
            )

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

        event = WorkflowEvent(
            type="workflow.started",
            timestamp=datetime.now(UTC),
            workflow_id=workflow.id,
            workflow_version=workflow.version,
            instance_id=instance.id,
        )

        context.events.append(
            event,
        )

        self._emit_event(
            event,
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

        context.execution_queue.append(
            workflow.start_node,
        )

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

        task = context.task

        if task is not None and getattr(
            task,
            "completed",
            False,
        ):
            node = instance.workflow.get(
                task.node_id,
            )

            context.execution_queue.extend(
                node.next_nodes,
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
                elapsed = datetime.now(UTC) - context.started_at

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

            if not context.execution_queue:
                context.completed = True
                break

            node = workflow.get(
                context.execution_queue.pop(0),
            )

            #
            # Reset retry counter
            #

            context.retry_attempt = 0

            #
            # Node started
            #

            event = WorkflowEvent(
                type="node.started",
                timestamp=datetime.now(UTC),
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                instance_id=instance.id,
                node_id=node.id,
            )

            context.events.append(
                event,
            )

            self._emit_event(
                event,
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

                if instance.project is None:
                    return self._failure(
                        instance,
                        "Workflow has no project.",
                    )

                child_workflow = instance.project.workflow(
                    context.subworkflow,
                )

                if child_workflow is None:
                    return self._failure(
                        instance,
                        f"Subworkflow '{context.subworkflow}' not found.",
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
            # Waiting?
            #
            # JoinNode uses waiting internally, but it should not pause
            # the whole workflow like WaitNode does.
            #

            if context.waiting:

                if node.__class__.__name__ == "JoinNode":
                    #
                    # Branch finished.
                    #
                    continue

                return WorkflowResult(
                    success=True,
                    output=context.variables,
                )

            #
            # Node completed
            #

            event = WorkflowEvent(
                type="node.completed",
                timestamp=datetime.now(UTC),
                workflow_id=workflow.id,
                workflow_version=workflow.version,
                instance_id=instance.id,
                node_id=node.id,
            )

            context.events.append(
                event,
            )

            self._emit_event(
                event,
            )

            #
            # Next node
            #

            if context.current_node is not None:
                context.execution_queue.append(
                    context.current_node,
                )

                context.current_node = None

            else:
                context.execution_queue.extend(
                    node.next_nodes,
                )

        #
        # Workflow completed
        #

        context.finished_at = datetime.now(UTC)

        event = WorkflowEvent(
            type="workflow.completed",
            timestamp=context.finished_at,
            workflow_id=workflow.id,
            workflow_version=workflow.version,
            instance_id=instance.id,
        )

        context.events.append(
            event,
        )

        self._emit_event(
            event,
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
        node: WorkflowNode,
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
        context.finished_at = datetime.now(UTC)

        #
        # Workflow failed event
        #

        event = WorkflowEvent(
            type="workflow.failed",
            timestamp=context.finished_at,
            workflow_id=workflow.id,
            workflow_version=workflow.version,
            instance_id=instance.id,
        )

        context.events.append(
            event,
        )

        self._emit_event(
            event,
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