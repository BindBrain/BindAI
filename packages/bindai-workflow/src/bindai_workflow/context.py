from __future__ import annotations

from datetime import UTC, datetime

from bindai_core.context import Variables

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .instance import WorkflowInstance
    
class WorkflowContext:
    """
    Shared execution context
    for one workflow instance.
    """

    def __init__(self):

        #
        # Workflow variables
        #

        self.variables = Variables()

        #
        # Execution queue
        #

        self.execution_queue: list[str] = []

        self.current_node: str | None = None

        self.completed = False

        #
        # Sub workflow
        #

        self.subworkflow = None

        #
        # Join nodes
        #

        self.join_state: dict[str, int] = {}

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
        # Runtime
        #

        self.errors: list[str] = []

        #
        # Execution events
        #

        self.events: list = []

        self.waiting = False

        self.task = None

        self.instance: WorkflowInstance | None = None

        self.retry_attempt = 0

        self.retry_policy = None

        self.timeout_policy = None

        #
        # Dependency Injection
        #

        self.services = None

        #
        # Compensation
        #

        from collections.abc import Callable

        self.compensations: list[Callable] = []

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
        name,
        value,
    ):

        self.variables.set(
            name,
            value,
        )
