# BindAI Task

`bindai-task` provides task abstractions for the BindAI framework.

It represents executable units of work together with task state and task result types.

## Features

* Task abstraction
* Task execution state
* Task execution results
* Reusable task contracts
* Integration with BindAI execution and workflow components

## Public API

The package exposes:

```python id="7m4q2x"
from bindai_task import (
    Task,
    TaskResult,
    TaskState,
)
```

## Task

`Task` represents a unit of work in BindAI.

```python id="3r8n6v"
from bindai_task import Task
```

Tasks can be used as building blocks for higher-level execution systems such as workflows and agent-oriented processes.

## Task State

`TaskState` represents the state associated with a task during its lifecycle.

```python id="9k2p5w"
from bindai_task import TaskState
```

Keeping task state separate from the task itself allows execution state to be managed independently from the task definition.

## Task Results

`TaskResult` represents the outcome of task execution.

```python id="5x7c1m"
from bindai_task import TaskResult
```

This provides a dedicated result abstraction for communicating task execution outcomes.

## Architecture

The package separates task definition, execution state, and execution results:

```text id="8v3n6q"
       Task
        │
        ▼
    TaskState
        │
        ▼
   TaskResult
```

These abstractions can then be consumed by higher-level BindAI execution components.

## BindAI Integration

`bindai-task` is a foundational package for representing units of work within BindAI.

It can be used by workflow and execution components while keeping task definitions separate from the systems responsible for coordinating execution.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="4m8q2r"
uv sync
```

Run the complete test suite:

```bash id="6n3v7x"
uv run pytest
```

Run static type checking for this package:

```bash id="1p5k9c"
uv run mypy packages/bindai-task
```

Build the package:

```bash id="7x2m4q"
uv build --package bindai-task
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
