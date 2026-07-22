from __future__ import annotations

from dataclasses import dataclass

from .event import Event
from .event_types import EventTypes


@dataclass(slots=True)
class ToolExecutedEvent(Event):

    tool_name: str

    @property
    def name(self):
        return EventTypes.TOOL_EXECUTED