from __future__ import annotations

from copy import deepcopy

from .history import AutomationRunHistory
from .run import AutomationRun


class MemoryAutomationRunHistory(AutomationRunHistory):
    """
    In-memory history for automation runs.

    Stored runs are copied so later mutations to an AutomationRun do not
    alter the historical record.
    """

    def __init__(self) -> None:
        self.runs: dict[str, AutomationRun] = {}

    def record(self, run: AutomationRun) -> None:
        self.runs[run.id] = deepcopy(run)

    def get(self, run_id: str) -> AutomationRun | None:
        run = self.runs.get(run_id)
        if run is None:
            return None
        return deepcopy(run)

    def list(self) -> tuple[AutomationRun, ...]:
        return tuple(deepcopy(run) for run in self.runs.values())
