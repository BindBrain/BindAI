from __future__ import annotations

from bindai_core.events import AgentStartedEvent, EventBus
from bindai_runtime.event_recorder import EventRecorder


def test_recorder_captures_events() -> None:
    bus = EventBus()
    recorder = EventRecorder(bus)

    event = AgentStartedEvent(
        payload={
            "agent": "test-agent",
            "execution_id": "execution-1",
        }
    )

    bus.publish(event)

    assert recorder.all() == [event]
    assert recorder.for_execution("execution-1") == [event]


def test_recorder_groups_events_by_execution() -> None:
    bus = EventBus()
    recorder = EventRecorder(bus)

    first = AgentStartedEvent(payload={"execution_id": "execution-1"})
    second = AgentStartedEvent(payload={"execution_id": "execution-2"})
    third = AgentStartedEvent(payload={"execution_id": "execution-1"})

    bus.publish(first)
    bus.publish(second)
    bus.publish(third)

    assert recorder.for_execution("execution-1") == [first, third]
    assert recorder.for_execution("execution-2") == [second]


def test_recorder_clear() -> None:
    bus = EventBus()
    recorder = EventRecorder(bus)

    event = AgentStartedEvent(payload={"execution_id": "execution-1"})
    bus.publish(event)

    recorder.clear()

    assert recorder.all() == []
    assert recorder.for_execution("execution-1") == []


def test_recorder_close_stops_recording() -> None:
    bus = EventBus()
    recorder = EventRecorder(bus)

    first = AgentStartedEvent(payload={"execution_id": "execution-1"})
    bus.publish(first)

    recorder.close()

    second = AgentStartedEvent(payload={"execution_id": "execution-1"})
    bus.publish(second)

    assert recorder.all() == [first]
