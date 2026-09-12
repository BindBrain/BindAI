from __future__ import annotations

from .run import AutomationRun
from .state_store import AutomationStateStore


class MemoryAutomationStateStore(AutomationStateStore):
    """
    In-memory persistence for automation runs.
    """

    def __init__(self) -> None:
        self.runs: dict[str, AutomationRun] = {}

    def save(self, run: AutomationRun) -> None:
        self.runs[run.id] = run

    def load(self, run_id: str) -> AutomationRun | None:
        return self.runs.get(run_id)

    def delete(self, run_id: str) -> None:
        self.runs.pop(run_id, None)
