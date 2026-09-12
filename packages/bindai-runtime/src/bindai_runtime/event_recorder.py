from __future__ import annotations

from collections import defaultdict
from threading import Lock

from bindai_core.events import Event, EventBus


class EventRecorder:
    """
    In-memory recorder for BindAI execution events.

    The recorder attaches to an existing EventBus and keeps the events
    emitted through that bus. It is intentionally lightweight so it can
    serve as the foundation for future tracing and metrics integrations.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._events: list[Event] = []
        self._events_by_execution: dict[str, list[Event]] = defaultdict(list)
        self._lock = Lock()

        self._event_bus = event_bus
        self._event_bus.subscribe("*", self.record)

    def record(self, event: Event) -> None:
        """Record an event emitted by the attached EventBus."""
        with self._lock:
            self._events.append(event)

            execution_id = event.payload.get("execution_id")
            if isinstance(execution_id, str):
                self._events_by_execution[execution_id].append(event)

    def all(self) -> list[Event]:
        """Return all recorded events in emission order."""
        with self._lock:
            return list(self._events)

    def for_execution(self, execution_id: str) -> list[Event]:
        """Return recorded events for a specific execution."""
        with self._lock:
            return list(self._events_by_execution.get(execution_id, ()))

    def clear(self) -> None:
        """Remove all recorded events."""
        with self._lock:
            self._events.clear()
            self._events_by_execution.clear()

    def close(self) -> None:
        """Detach the recorder from the EventBus."""
        self._event_bus.unsubscribe("*", self.record)
