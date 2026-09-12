# BindAI Automation

Automation definitions, execution state, run history, background execution, and event-trigger primitives for BindAI.

## Automation Definitions

`AutomationDefinition` describes an automation and the executable target it invokes.

```python
from bindai_automation import AutomationDefinition

automation = AutomationDefinition(
    name="my-automation",
    target=my_executable,
)

result = automation.run()
```

Each definition provides:

* `id` — unique automation definition identifier
* `name` — human-readable automation name
* `version` — definition version, starting at `1`
* `target` — the `bindai-core` executable invoked by the automation
* `metadata` — optional application-defined metadata

Definitions can be cloned to create a new version:

```python
version_2 = automation.clone()

assert version_2.version == 2
assert automation.version == 1
```

The automation definition is intentionally independent from triggers. A definition describes **what runs**, while triggers describe **when it runs**.

## Automation Runs

`AutomationRun` represents one execution of an automation definition.

```python
from bindai_automation import AutomationRun

run = AutomationRun(
    definition_id=automation.id,
    definition_version=automation.version,
    input={"message": "hello"},
)

run.start()

# Execute the automation target here.

run.complete(output={"result": "done"})
```

An automation run provides:

* `id` — unique execution identifier
* `definition_id` — automation definition identifier
* `definition_version` — definition version used for the execution
* `status` — execution state such as `pending`, `running`, `completed`, or `failed`
* `input` — optional execution input
* `output` — execution output
* `error` — failure information when execution fails
* `created_at` — run creation timestamp
* `started_at` — execution start timestamp
* `completed_at` — execution completion timestamp

Runs expose lifecycle methods:

```python
run.start()

run.complete(output={"result": "done"})

run.fail("execution failed")
```

The run object represents execution state independently from the automation definition itself.

## Automation State Store

`AutomationStateStore` defines the persistence contract for automation runs.

```python
from bindai_automation import AutomationStateStore


class CustomAutomationStateStore(AutomationStateStore):
    def save(self, run): ...

    def load(self, run_id): ...

    def delete(self, run_id): ...
```

The state store is intentionally separate from `AutomationRun`. This allows execution state to be stored in memory or backed by another persistence system without coupling the run model to a specific storage implementation.

## In-Memory State Store

`MemoryAutomationStateStore` provides an in-memory implementation of the automation state store.

```python
from bindai_automation import MemoryAutomationStateStore

store = MemoryAutomationStateStore()

store.save(run)

loaded = store.load(run.id)

assert loaded is run
```

Runs can also be removed:

```python
store.delete(run.id)

assert store.load(run.id) is None
```

The in-memory store is intended as a lightweight implementation and as a foundation for future persistent storage backends.

## Automation Run History

`AutomationRunHistory` defines the history contract for recording and retrieving automation runs.

```python
from bindai_automation import AutomationRunHistory


class CustomAutomationRunHistory(AutomationRunHistory):
    def record(self, run): ...

    def get(self, run_id): ...

    def list(self): ...
```

Run history is intentionally separate from `AutomationStateStore`.

The state store answers:

> Where is the current execution state of this run?

Run history answers:

> What automation runs have been recorded?

This separation allows current execution state and historical records to evolve independently.

The history contract provides:

* `record(run)` — record an automation run
* `get(run_id)` — retrieve a historical run by ID
* `list()` — retrieve recorded runs in insertion order

## In-Memory Run History

`MemoryAutomationRunHistory` provides an in-memory implementation of `AutomationRunHistory`.

```python
from bindai_automation import MemoryAutomationRunHistory

history = MemoryAutomationRunHistory()

run = AutomationRun(
    definition_id=automation.id,
    definition_version=automation.version,
)

run.start()
run.complete(output={"result": "done"})

history.record(run)

stored = history.get(run.id)

assert stored is not None
assert stored.id == run.id
```

Recorded runs are stored as snapshots. Later changes to the original `AutomationRun` do not modify the historical record.

```python
run.output = {"result": "changed"}

stored = history.get(run.id)

assert stored is not None
assert stored.output == {"result": "done"}
```

The in-memory implementation is intentionally lightweight and provides the foundation for future persistent run-history backends.

## Automation Worker

`AutomationWorker` executes automation definitions either synchronously or in background threads.

### Synchronous execution

```python
from bindai_automation import AutomationWorker

worker = AutomationWorker()

run = worker.run(automation)

assert run.status == "completed"
```

### Background execution

Use `submit()` to execute an automation in the worker thread pool:

```python
worker = AutomationWorker(max_workers=4)

future = worker.submit(automation)

run = future.result(timeout=5)

assert run.status == "completed"
```

The worker manages the lifecycle of each `AutomationRun`:

1. Creates the run.
2. Persists its initial state.
3. Marks the run as `running`.
4. Executes the automation definition.
5. Records success or failure.
6. Persists the final state.
7. Records the completed or failed run in history.

Custom state and history implementations can be supplied:

```python
worker = AutomationWorker(
    state_store=custom_state_store,
    history=custom_history,
)
```

Workers should be shut down when they are no longer needed:

```python
worker.shutdown()
```

They can also be used as context managers:

```python
with AutomationWorker() as worker:
    run = worker.run(automation)
```

The current worker provides lightweight in-process background execution using Python's `ThreadPoolExecutor`. Distributed workers, durable queues, and persistent worker infrastructure are future capabilities.

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

The registry stores trigger instances; registering a trigger does not automatically attach it to its event source.

## Current Scope

The package currently provides:

* `AutomationDefinition` — definition and versioning of an executable automation
* `AutomationRun` — execution state for an automation run
* `AutomationStateStore` — persistence contract for automation runs
* `MemoryAutomationStateStore` — in-memory automation state implementation
* `AutomationRunHistory` — history contract for recorded automation runs
* `MemoryAutomationRunHistory` — in-memory automation run-history implementation
* `AutomationWorker` — synchronous and in-process background automation execution
* `Trigger` — base trigger abstraction
* `EventTrigger` — event-driven trigger implementation
* `TriggerRegistry` — registry for named triggers

These primitives provide the foundation for stateful, historical, event-driven automation in BindAI.

## Current Limitations

The package currently does not provide:

* persistent database-backed automation state
* persistent database-backed run history
* distributed or durable background workers
* built-in scheduled execution
* advanced event routing
* built-in retry policies
* distributed execution queues
* durable workflow recovery

These capabilities can be added on top of the existing automation contracts without coupling the core run model to a specific persistence or execution infrastructure.
