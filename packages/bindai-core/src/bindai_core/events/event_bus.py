from collections import defaultdict

from .event import Event
from .event_handler import EventHandler


class EventBus:
    """
    Simple synchronous event bus.
    """

    def __init__(self):

        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:

        self._handlers[event_name].append(handler)

    def publish(self, event: Event) -> None:

        for handler in self._handlers[event.name]:
            handler(event)