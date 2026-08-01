from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from bindai_core.context import Variables

if TYPE_CHECKING:
    from .instance import WorkflowInstance

from .retry import RetryPolicy
from .timeout import TimeoutPolicy


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

        self.user: str | None = None
        self.tenant: str | None = None
        self.project: object | None = None
        self.application: str | None = None

        #
        # Runtime
        #

        self.errors: list[str] = []

        #
        # Execution events
        #

        self.events: list[object] = []

        self.waiting = False

        self.task: object | None = None

        self.instance: WorkflowInstance | None = None

        self.retry_attempt = 0

        self.retry_policy: RetryPolicy | None = None

        self.timeout_policy: TimeoutPolicy | None = None

        #
        # Dependency Injection
        #

        self.services = None

        #
        # Compensation
        #

        self.compensations: list[Callable[..., None]] = []

    def get(
        self,
        name: str,
        default: object | None = None,
    ) -> object:

        return self.variables.get(
            name,
            default,
        )

    def set(
        self,
        name: str,
        value: object,
    ) -> None:

        self.variables.set(
            name,
            value,
        )
