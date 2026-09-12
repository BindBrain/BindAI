from dataclasses import dataclass

import pytest
from bindai_automation import EventTrigger
from bindai_automation.registry import TriggerRegistry
from bindai_core.events import Event, EventBus


@dataclass(slots=True, kw_only=True)
class RegistryEvent(Event):
    @property
    def name(self) -> str:
        return "registry.event"


def create_trigger() -> EventTrigger:
    return EventTrigger(
        bus=EventBus(),
        event_name="registry.event",
        target=lambda event: None,
    )


def test_register_and_get():
    registry = TriggerRegistry()
    trigger = create_trigger()
    registry.register("test", trigger)
    assert registry.get("test") is trigger


def test_duplicate_registration_fails():
    registry = TriggerRegistry()
    trigger = create_trigger()
    registry.register("test", trigger)
    with pytest.raises(ValueError):
        registry.register("test", trigger)


def test_get_or_none():
    registry = TriggerRegistry()
    assert registry.get_or_none("missing") is None


def test_remove():
    registry = TriggerRegistry()
    trigger = create_trigger()
    registry.register("test", trigger)
    registry.remove("test")
    assert not registry.contains("test")


def test_clear():
    registry = TriggerRegistry()
    registry.register("one", create_trigger())
    registry.register("two", create_trigger())
    registry.clear()
    assert len(registry) == 0


def test_keys_values_and_items():
    registry = TriggerRegistry()
    first = create_trigger()
    second = create_trigger()
    registry.register("one", first)
    registry.register("two", second)
    assert registry.keys() == ("one", "two")
    assert registry.values() == (first, second)
    assert registry.items() == (
        ("one", first),
        ("two", second),
    )
