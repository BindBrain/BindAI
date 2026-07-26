from __future__ import annotations

from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_core.model.request import ModelRequest
    from bindai_core.model.response import ModelResponse

from .event import Event
from .event_types import EventTypes


@dataclass(slots=True)
class ModelRequestEvent(Event):

    request: ModelRequest

    @property
    def name(self) -> str:
        return EventTypes.MODEL_REQUESTED


@dataclass(slots=True)
class ModelResponseEvent(Event):

    response: ModelResponse

    @property
    def name(self) -> str:
        return EventTypes.MODEL_RESPONDED
