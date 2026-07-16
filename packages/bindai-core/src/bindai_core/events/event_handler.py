from typing import Protocol

from .event import Event


class EventHandler(Protocol):

    def __call__(self, event: Event) -> None:
        ...