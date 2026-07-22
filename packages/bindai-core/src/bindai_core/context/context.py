from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from bindai_core.container import BindContainer
from bindai_core.events import EventBus
from bindai_core.registry import Registry

from .state import ExecutionState
from .variables import Variables


@dataclass(slots=True)
class ExecutionContext:
    """
    Carries everything required during execution.
    """

    execution_id: str = field(default_factory=lambda: str(uuid4()))

    state: ExecutionState = ExecutionState.CREATED

    container: BindContainer = field(default_factory=BindContainer)

    registry: Registry = field(default_factory=Registry)

    events: EventBus = field(default_factory=EventBus)

    variables: Variables = field(default_factory=Variables)

    metadata: dict = field(
        default_factory=dict,
    )

    data: object | None = None
