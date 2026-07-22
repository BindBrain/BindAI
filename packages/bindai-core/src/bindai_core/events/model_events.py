from __future__ import annotations

from dataclasses import dataclass

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)

from .event import Event
from .event_types import EventTypes


@dataclass(slots=True)
class ModelRequestEvent(Event):

    request: ModelRequest

    @property
    def name(self) -> str:
        return EventTypes.MODEL_INVOKED


@dataclass(slots=True)
class ModelResponseEvent(Event):

    response: ModelResponse

    @property
    def name(self) -> str:
        return EventTypes.MODEL_INVOKED