# BindAI Project

`bindai-project` provides the project-level container for organizing a BindAI solution.

A `Project` brings together applications, shared tools, workflows, scheduling, configuration, and other project-wide resources under a single object.

## Features

* Project configuration
* Application management
* Shared tool registration
* Workflow management
* Workflow scheduling
* Application execution
* Streaming execution
* Project-wide resource containers

## Public API

The package exposes:

```python
from bindai_project import (
    Project,
    ProjectBuilder,
    ProjectConfiguration,
)
```

## Creating a Project

The recommended entry point is `ProjectBuilder`:

```python
from bindai_project import ProjectBuilder

project = (
    ProjectBuilder("my-project")
    .build()
)
```

The builder can also register applications and shared tools:

```python
project = (
    ProjectBuilder("my-project")
    .application(application)
    .tool(tool)
    .build()
)
```

## Applications

Projects can contain multiple applications.

```python
project.add_application(application)
```

Applications are stored by their name and can be retrieved with:

```python
application = project.application("my-application")
```

A project can also execute an agent through one of its applications:

```python
result = project.run(
    application="my-application",
    agent="assistant",
    message="Hello!",
)
```

Streaming execution is available through `stream()`:

```python
stream = project.stream(
    application="my-application",
    agent="assistant",
    message="Hello!",
)
```

## Shared Tools

Projects provide a shared tool registry.

```python
project.add_tool(tool)
```

Shared tools are managed through the project's `ToolRegistry`.

This allows tools to be registered at project scope rather than being tied to a single application.

## Workflows

Projects can contain workflows through `WorkflowRegistry`.

```python
project.add_workflow(workflow)
```

A workflow can be retrieved by its identifier:

```python
workflow = project.workflow("workflow-id")
```

Projects also expose a `WorkflowScheduler` for project-level scheduling.

```python
project.add_schedule(schedule)
```

## Project Resources

The `Project` object provides project-level containers for resources that can be associated with a BindAI solution:

```text
Project
├── Configuration
├── Applications
├── Shared Tools
├── Workflows
├── Workflow Scheduler
├── Knowledge
├── Memories
└── Secrets
```

Knowledge, memories, and secrets are currently represented as project-level resource containers, allowing the project architecture to accommodate these resources independently of applications.

## Architecture

The project layer sits above individual BindAI components:

```text
Project
   │
   ├── Applications
   │      └── Agents
   │
   ├── Shared Tools
   │
   ├── Workflows
   │      └── Workflow Scheduler
   │
   └── Project Resources
          ├── Knowledge
          ├── Memories
          └── Secrets
```

The project therefore acts as a root container for a complete BindAI solution while allowing the underlying components to remain independently reusable.

## Python Helpers

Projects support convenient Python container operations.

Membership checks whether an application exists:

```python
if "my-application" in project:
    ...
```

The number of registered applications can be obtained with:

```python
count = len(project)
```

Projects can also be iterated over to access their applications:

```python
for application in project:
    ...
```

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash
uv sync
```

Run the complete test suite:

```bash
uv run pytest
```

Run static type checking for this package:

```bash
uv run mypy packages/bindai-project
```

Build the package:

```bash
uv build --package bindai-project
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
