# BindAI Automation

Automation and event-trigger primitives for BindAI.

## Event Triggers

`EventTrigger` listens to a `bindai-core` event bus and invokes a callable target when the configured event is published.

```python
from bindai_automation import EventTrigger
from bindai_core.events import EventBus, Event


class MyEvent(Event):
    @property
    def name(self) -> str:
        return "my.event"


bus = EventBus()


def handle_event(event):
    print("Automation triggered:", event.payload)


trigger = EventTrigger(
    bus=bus,
    event_name="my.event",
    target=handle_event,
)

trigger.attach()

bus.publish(
    MyEvent(
        payload={"message": "hello"},
    )
)
```

### Enable and disable

Triggers can be temporarily disabled without detaching them:

```python
trigger.disable()

trigger.enable()
```

A disabled trigger remains attached to the event bus but does not invoke its target.

### Detach

A trigger can be detached from the event bus when it is no longer needed:

```python
trigger.detach()
```

Calling `attach()` more than once does not create duplicate subscriptions.

## Trigger Registry

`TriggerRegistry` provides a registry for named automation triggers.

```python
from bindai_automation import EventTrigger, TriggerRegistry
from bindai_core.events import EventBus


bus = EventBus()

trigger = EventTrigger(
    bus=bus,
    event_name="my.event",
    target=handle_event,
)

registry = TriggerRegistry()

registry.register(
    "my-trigger",
    trigger,
)

registered = registry.get("my-trigger")
```

The registry supports:

```python
registry.get("my-trigger")
registry.get_or_none("my-trigger")
registry.contains("my-trigger")

registry.keys()
registry.values()
registry.items()

registry.remove("my-trigger")
registry.clear()
```

The registry stores trigger definitions; registering a trigger does not automatically attach it to its event source.

## Current Scope

The package currently provides:

* `Trigger` — base trigger abstraction
* `EventTrigger` — event-driven trigger implementation
* `TriggerRegistry` — registry for named triggers

These primitives provide the foundation for event-driven automation in BindAI.

The package currently does not provide persistent automation state, background workers, scheduled execution, or built-in retry handling.
