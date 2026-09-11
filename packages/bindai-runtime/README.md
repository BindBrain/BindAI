# BindAI Runtime

`bindai-runtime` provides the runtime layer for executing BindAI components.

The runtime coordinates execution context, executor resolution, and scheduling through a small set of runtime components.

## Features

* Central BindAI runtime
* Execution context management
* Executor resolution
* Executor registry
* Basic task scheduling
* Runtime integration with executable components

## Public API

The package exposes:

```python id="7m2q8v"
from bindai_runtime import BindRuntime
```

## BindRuntime

`BindRuntime` is the main runtime entry point.

```python id="4k8n3x"
from bindai_runtime import BindRuntime

runtime = BindRuntime()
```

A runtime provides the execution context, executor registry, execution engine, and scheduler used by the BindAI runtime layer.

## Executing Components

The runtime can execute a supported BindAI executable:

```python id="9p5r2w"
result = runtime.run(executable)
```

The runtime creates and maintains an `ExecutionContext` and delegates execution to the appropriate executor.

## Execution Architecture

The runtime resolves an executor for the executable being run:

```text id="6v1m8q"
BindRuntime
    │
    ├── ExecutionContext
    │
    ├── ExecutorRegistry
    │       │
    │       └── resolves executor
    │
    ├── ExecutionEngine
    │       │
    │       └── executes component
    │
    └── Scheduler
            │
            └── queued execution
```

`ExecutorRegistry` maps executable types to their corresponding executor implementations.

`ExecutionEngine` resolves the appropriate executor and executes the component using the runtime context.

## Scheduler

The runtime also exposes a scheduler for submitting executable components for later processing.

```python id="2x7c4n"
runtime.scheduler.submit(executable)
```

The scheduler provides a simple queue-based execution mechanism. Background automation workers are implemented separately by `bindai-automation`.

## Runtime and Executables

The runtime works with BindAI's common executable architecture.

This keeps execution orchestration separate from individual components such as agents, workflows, and other executable resources.

```text id="8q3n5m"
Executable
    │
    ▼
BindRuntime
    │
    ▼
ExecutionEngine
    │
    ▼
ExecutorRegistry
    │
    ▼
Executor
```

## BindAI Integration

`bindai-runtime` is a foundational runtime package used to coordinate execution across the BindAI platform.

It focuses on execution infrastructure rather than implementing application-specific or provider-specific behavior.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="5n7r2x"
uv sync
```

Run the complete test suite:

```bash id="1q8m4v"
uv run pytest
```

Run static type checking for this package:

```bash id="6x3k9p"
uv run mypy packages/bindai-runtime
```

Build the package:

```bash id="9v2c5n"
uv build --package bindai-runtime
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
