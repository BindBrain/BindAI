from __future__ import annotations

from dataclasses import dataclass

from .event import Event
from .event_types import EventTypes


@dataclass(slots=True)
class WorkflowStartedEvent(Event):
    @property
    def name(self) -> str:
        return EventTypes.WORKFLOW_STARTED


@dataclass(slots=True)
class WorkflowFinishedEvent(Event):
    @property
    def name(self) -> str:
        return EventTypes.WORKFLOW_FINISHED


@dataclass(slots=True)
class WorkflowFailedEvent(Event):
    @property
    def name(self) -> str:
        return EventTypes.WORKFLOW_FAILED


@dataclass(slots=True)
class NodeStartedEvent(Event):
    @property
    def name(self) -> str:
        return EventTypes.NODE_STARTED


@dataclass(slots=True)
class NodeCompletedEvent(Event):
    @property
    def name(self) -> str:
        return EventTypes.NODE_COMPLETED