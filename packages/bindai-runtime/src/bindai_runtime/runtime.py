from __future__ import annotations

from bindai_core.context import ExecutionContext

from .bootstrap import create_registry
from .engine import ExecutionEngine
from .event_recorder import EventRecorder
from .scheduler import Scheduler


class BindRuntime:
    """
    Central runtime for BindAI.
    """

    def __init__(self):
        self.context = ExecutionContext()
        self.registry = create_registry()
        self.engine = ExecutionEngine(
            self.registry,
        )
        self.scheduler = Scheduler()
        self.observability = EventRecorder(
            self.context.events,
        )

    def run(
        self,
        executable,
    ):
        return self.engine.execute(
            executable,
            self.context,
        )
