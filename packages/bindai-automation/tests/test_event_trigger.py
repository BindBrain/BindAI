from dataclasses import dataclass

from bindai_automation.event_trigger import EventTrigger
from bindai_core.events import Event, EventBus


@dataclass(slots=True, kw_only=True)
class SampleEvent(Event):
    @property
    def name(self) -> str:
        return "test.event"


@dataclass(slots=True, kw_only=True)
class OtherSampleEvent(Event):
    @property
    def name(self) -> str:
        return "other.event"


def test_event_trigger_calls_target():
    bus = EventBus()
    received = []

    def target(event):
        received.append(event)

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()

    event = SampleEvent(
        payload={"value": 42},
    )

    bus.publish(event)

    assert received == [event]


def test_event_trigger_ignores_other_events():
    bus = EventBus()
    received = []

    def target(event):
        received.append(event)

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()

    bus.publish(
        OtherSampleEvent(),
    )

    assert received == []


def test_disabled_trigger_does_not_execute():
    bus = EventBus()
    received = []

    def target(event):
        received.append(event)

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()
    trigger.disable()

    bus.publish(
        SampleEvent(),
    )

    assert received == []


def test_detached_trigger_does_not_execute():
    bus = EventBus()
    received = []

    def target(event):
        received.append(event)

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()
    trigger.detach()

    bus.publish(
        SampleEvent(),
    )

    assert received == []


def test_attach_is_idempotent():
    bus = EventBus()
    received = []

    def target(event):
        received.append(event)

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()
    trigger.attach()

    event = SampleEvent()

    bus.publish(event)

    assert received == [event]


def test_detach_is_idempotent():
    bus = EventBus()

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=lambda event: None,
    )

    trigger.attach()
    trigger.detach()
    trigger.detach()


def test_event_trigger_can_start_runtime_executable():
    bus = EventBus()
    executed = []

    def target(event):
        executed.append(event.payload)

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()

    bus.publish(
        SampleEvent(
            payload={"action": "run"},
        )
    )

    assert executed == [{"action": "run"}]


def test_target_failure_does_not_break_event_bus():
    bus = EventBus()
    received = []

    def target(event):
        received.append(event)
        raise RuntimeError("boom")

    trigger = EventTrigger(
        bus=bus,
        event_name="test.event",
        target=target,
    )

    trigger.attach()

    event = SampleEvent()

    bus.publish(event)

    assert received == [event]
