from __future__ import annotations

from datetime import UTC, datetime

from bindai_core.context import Variables


class WorkflowContext:
    """
    Runtime state for one workflow execution.

    The Workflow definition is immutable.
    Everything that changes during execution
    lives here.
    """

    def __init__(self) -> None:

        #
        # Variables
        #

        self.variables = Variables()

        #
        # Execution
        #

        self.current_node: str | None = None

        self.completed = False

        self.success = False

        self.waiting = False

        #
        # Parallel execution
        #

        self.parallel_nodes: list[str] = []

        #
        # Nested workflows
        #

        self.subworkflow = None

        #
        # Retry
        #

        self.retry_attempt = 0

        self.retry_policy = None

        #
        # Timeout
        #

        self.timeout_policy = None

        #
        # Compensation
        #

        self.compensations: list = []

        #
        # Events
        #

        self.events: list = []

        #
        # Errors
        #

        self.errors: list[str] = []

        #
        # Runtime ownership
        #

        self.instance = None

        self.task = None

        #
        # Lifecycle
        #

        self.started_at = datetime.now(UTC)

        self.finished_at: datetime | None = None

        #
        # Identity
        #

        self.user = None

        self.tenant = None

        self.project = None

        self.application = None

    #
    # Variables
    #

    def get(
        self,
        name: str,
        default=None,
    ):
        return self.variables.get(
            name,
            default,
        )

    def set(
        self,
        name: str,
        value,
    ) -> None:
        self.variables.set(
            name,
            value,
        )

    def contains(
        self,
        name: str,
    ) -> bool:
        return self.variables.contains(
            name,
        )

    #
    # Errors
    #

    def add_error(
        self,
        error: str,
    ) -> None:
        self.errors.append(error)

    #
    # Events
    #

    def publish(
        self,
        event,
    ) -> None:
        self.events.append(event)