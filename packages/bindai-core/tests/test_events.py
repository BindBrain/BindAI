from bindai_core.events import (
    Event,
    EventBus,
)


def test_publish_event():

    bus = EventBus()

    received = []

    def handler(event):

        received.append(event.name)

    bus.subscribe(
        "hello",
        handler,
    )

    bus.publish(Event("hello"))

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

    bus.publish(Event("go"))

    assert len(count) == 2
