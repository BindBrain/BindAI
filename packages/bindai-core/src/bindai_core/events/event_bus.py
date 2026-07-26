from collections import defaultdict
import logging

from .event import Event
from .event_handler import EventHandler


logger = logging.getLogger(__name__)


class EventBus:
    """
    Simple synchronous event bus.
    """

    def __init__(self):

        self._handlers: dict[
            str,
            list[EventHandler],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:

        self._handlers[event_name].append(
            handler,
        )

    def unsubscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:

        if handler in self._handlers[event_name]:
            self._handlers[event_name].remove(
                handler,
            )

    def publish(
        self,
        event: Event,
    ) -> None:

        handlers = self._handlers[event.name] + self._handlers["*"]

        for handler in handlers:
            try:
                handler(event)

            except Exception:
                logger.exception(
                    "Event handler failed."
                )