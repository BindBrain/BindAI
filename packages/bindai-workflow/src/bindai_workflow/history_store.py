from __future__ import annotations

from .history import WorkflowHistory


class MemoryHistoryStore:
    def __init__(self):

        self._history: list[WorkflowHistory] = []

    def add(
        self,
        history: WorkflowHistory,
    ):

        self._history.append(
            history,
        )

    def all(
        self,
    ) -> list[WorkflowHistory]:

        return list(self._history)

    def workflow(
        self,
        workflow_id: str,
    ):

        return [item for item in self._history if item.workflow_id == workflow_id]
