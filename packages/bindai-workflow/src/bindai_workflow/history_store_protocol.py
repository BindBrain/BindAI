from __future__ import annotations

from typing import Protocol

from .history import WorkflowHistory


class WorkflowHistoryStore(Protocol):
    def add(
        self,
        history: WorkflowHistory,
    ) -> None: ...

    def all(
        self,
    ) -> list[WorkflowHistory]: ...

    def workflow(
        self,
        workflow_id: str,
    ) -> list[WorkflowHistory]: ...
