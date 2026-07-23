from dataclasses import dataclass

from bindai_core.events import (
    Event,
    EventBus,
)


@dataclass(slots=True, kw_only=True)
class HelloEvent(Event):

    @property
    def name(self) -> str:
        return "hello"


@dataclass(slots=True, kw_only=True)
class GoEvent(Event):

    @property
    def name(self) -> str:
        return "go"


def test_publish_event():

    bus = EventBus()

    received = []

    def handler(event):
        received.append(event.name)

    bus.subscribe(
        "hello",
        handler,
    )

    bus.publish(
        HelloEvent(),
    )

    assert received == ["hello"]


def test_multiple_handlers():

    bus = EventBus()

    count = []

    def a(event):
        count.append(1)

    def b(event):
        count.append(2)

    bus.subscribe(
        "go",
        a,
    )

    bus.subscribe(
        "go",
        b,
    )

    bus.publish(
        GoEvent(),
    )

    assert len(count) == 2