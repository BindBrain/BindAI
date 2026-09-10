from __future__ import annotations

from collections.abc import Callable

from bindai_core.events import Event, EventBus

from .trigger import Trigger


class EventTrigger(Trigger):
    """
    Trigger an action when a matching event is published.
    """

    def __init__(
        self,
        *,
        bus: EventBus,
        event_name: str,
        target: Callable[[Event], None],
    ) -> None:
        super().__init__()

        self.bus = bus
        self.event_name = event_name
        self.target = target
        self._attached = False

    def attach(self) -> None:
        if self._attached:
            return

        self.bus.subscribe(
            self.event_name,
            self._handle_event,
        )

        self._attached = True

    def detach(self) -> None:
        if not self._attached:
            return

        self.bus.unsubscribe(
            self.event_name,
            self._handle_event,
        )

        self._attached = False

    def _handle_event(
        self,
        event: Event,
    ) -> None:
        if not self.enabled:
            return

        self.target(event)