from __future__ import annotations

from dataclasses import dataclass

from .event import Event
from .event_types import EventTypes


@dataclass(slots=True)
class AgentStartedEvent(Event):
    @property
    def name(self):
        return EventTypes.AGENT_STARTED


@dataclass(slots=True)
class AgentFinishedEvent(Event):
    @property
    def name(self):
        return EventTypes.AGENT_FINISHED
