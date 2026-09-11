# BindAI Workflow

`bindai-workflow` provides workflow orchestration for the BindAI framework.

It provides the abstractions needed to define, execute, schedule, persist, serialize, deploy, and manage workflows composed of different types of execution nodes.

## Features

* Workflow definitions
* Workflow builder and configuration
* Workflow execution instances
* Workflow registries
* Workflow storage
* In-memory workflow storage
* Agent nodes
* Runnable nodes
* Conditional nodes
* Parallel execution
* Join nodes
* Loop nodes
* Sub-workflows
* Start and end nodes
* Human tasks
* Retry policies
* Timeout policies
* Workflow scheduling
* Compensation actions
* Workflow history
* Workflow repositories
* Serialization and deserialization
* Workflow deployment
* Workflow factories
* Workflow management services

## Public API

The package exposes the main workflow components directly:

```python id="7m4q2x"
from bindai_workflow import (
    Workflow,
    WorkflowBuilder,
    WorkflowConfiguration,
    WorkflowRegistry,
    WorkflowInstance,
    WorkflowStore,
    MemoryWorkflowStore,
)
```

Additional workflow infrastructure includes:

```python id="4r8n6v"
from bindai_workflow import (
    WorkflowFactory,
    WorkflowManager,
    WorkflowNodeFactory,
    WorkflowSerializer,
    WorkflowDeserializer,
    WorkflowRepository,
    WorkflowDeployment,
    WorkflowServices,
)
```

## Creating Workflows

`WorkflowBuilder` provides the builder API for constructing workflows.

```python id="8p3k1w"
from bindai_workflow import WorkflowBuilder

builder = WorkflowBuilder(...)
```

Workflow configuration is represented by `WorkflowConfiguration`.

```python id="2x7m5q"
from bindai_workflow import WorkflowConfiguration
```

The resulting `Workflow` represents the executable workflow definition.

## Workflow Nodes

Workflows can be composed from different node types.

The package exposes:

```text id="6n9v3r"
Workflow
   │
   ├── StartNode
   ├── AgentNode
   ├── RunnableNode
   ├── ConditionNode
   ├── ParallelNode
   ├── JoinNode
   ├── LoopNode
   ├── SubWorkflowNode
   ├── HumanTask
   ├── CompensationNode
   └── EndNode
```

These nodes allow workflows to represent different execution patterns and control-flow structures.

## Parallel Execution

`ParallelNode` provides parallel workflow execution, while `JoinNode` represents synchronization after parallel branches.

```python id="5q8c2m"
from bindai_workflow import (
    ParallelNode,
    JoinNode,
)
```

This makes it possible to model workflows where independent operations can execute concurrently before continuing to a later stage.

## Conditions and Loops

Conditional and iterative execution are supported through:

```python id="9v4k1x"
from bindai_workflow import (
    ConditionNode,
    LoopNode,
)
```

`WorkflowExpression` is also available for workflow expressions:

```python id="3m7p2n"
from bindai_workflow import WorkflowExpression
```

## Sub-Workflows

`SubWorkflowNode` allows a workflow to incorporate another workflow as part of its execution.

```python id="1x6r8q"
from bindai_workflow import SubWorkflowNode
```

This supports composing larger workflows from reusable workflow definitions.

## Human Tasks

`HumanTask` provides a workflow task abstraction for human-involved execution.

```python id="4n9w2k"
from bindai_workflow import HumanTask
```

This allows workflow definitions to represent work that is not performed entirely automatically.

## Retry and Timeout Policies

Workflow execution can use retry and timeout policies:

```python id="7c3m5v"
from bindai_workflow import (
    RetryPolicy,
    TimeoutPolicy,
)
```

These policies provide workflow-level execution controls without requiring every workflow node to implement its own retry or timeout behavior.

## Workflow Scheduling

Workflows can be scheduled through `WorkflowSchedule` and `WorkflowScheduler`.

```python id="8k2q6p"
from bindai_workflow import (
    WorkflowSchedule,
    WorkflowScheduler,
)
```

The scheduler provides the workflow-level scheduling abstraction, while the schedule represents the scheduling configuration.

## Workflow State and Instances

`WorkflowInstance` represents an execution instance of a workflow.

```python id="5r7m1x"
from bindai_workflow import WorkflowInstance
```

Workflow persistence is represented by `WorkflowStore`:

```python id="2p9v4n"
from bindai_workflow import WorkflowStore
```

BindAI also provides an in-memory implementation:

```python id="6x3k8q"
from bindai_workflow import MemoryWorkflowStore
```

This separation allows workflow execution state to be stored independently from the workflow definition.

## Workflow History

Workflow execution history is represented by `WorkflowHistory` and can be persisted through a history store.

```python id="9m5w2r"
from bindai_workflow import (
    WorkflowHistory,
    MemoryHistoryStore,
)
```

`MemoryHistoryStore` provides an in-memory history implementation.

## Serialization

Workflows can be serialized and deserialized through:

```python id="4q8n1v"
from bindai_workflow import (
    WorkflowSerializer,
    WorkflowDeserializer,
)
```

Factories are also available for constructing workflows:

```python id="7x2m6p"
from bindai_workflow import (
    WorkflowFactory,
    WorkflowNodeFactory,
)
```

## Compensation

Compensation actions support workflows that need explicit recovery or compensating behavior.

```python id="3n9r5k"
from bindai_workflow import (
    CompensationAction,
    CompensationNode,
)
```

## Workflow Management

Higher-level workflow management components include:

```python id="8v1c4q"
from bindai_workflow import (
    WorkflowManager,
    WorkflowServices,
)
```

These provide the management and service layer around workflow functionality.

## Architecture

The workflow package separates workflow definitions from execution state and supporting infrastructure:

```text id="6p3m8x"
Workflow
   │
   ├── Nodes
   │     ├── Agent
   │     ├── Runnable
   │     ├── Condition
   │     ├── Parallel
   │     ├── Join
   │     ├── Loop
   │     ├── SubWorkflow
   │     ├── Human Task
   │     └── Compensation
   │
   ├── WorkflowInstance
   │
   ├── WorkflowStore
   │
   ├── WorkflowHistory
   │
   └── WorkflowScheduler
```

Supporting components provide serialization, deployment, repositories, factories, and workflow management.

## BindAI Integration

`bindai-workflow` integrates with other BindAI packages to orchestrate executable components.

For example, workflow nodes can coordinate agents and runnable components while workflow state, scheduling, retry, timeout, and history concerns remain within the workflow layer.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="5k8m2q"
uv sync
```

Run the complete test suite:

```bash id="7r3n9v"
uv run pytest
```

Run static type checking for this package:

```bash id="2x6p4m"
uv run mypy packages/bindai-workflow
```

Build the package:

```bash id="9q1c7w"
uv build --package bindai-workflow
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
