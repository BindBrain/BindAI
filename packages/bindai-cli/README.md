# BindAI CLI

`bindai-cli` provides the command-line interface for creating, inspecting, developing, and managing BindAI projects.

The CLI is designed to provide a convenient developer workflow around the BindAI framework and its project structure.

## Features

The BindAI CLI provides commands for common development tasks, including:

* Project initialization
* Project scaffolding
* BindAI environment inspection
* Framework diagnostics
* Project creation
* Development utilities
* CLI-based project management

## Installation

The CLI is included as the `bindai-cli` package in the BindAI workspace.

For development from the BindAI repository:

```bash
uv sync
```

The CLI can then be executed with:

```bash
uv run bindai
```

## Common Commands

### Doctor

Run BindAI diagnostics:

```bash
bindai doctor
```

This command is intended to help identify configuration or environment issues.

### Inspect

Inspect the current BindAI environment or project:

```bash
bindai inspect
```

### Initialize

Initialize a BindAI project:

```bash
bindai init
```

### Create a Project

Create a new BindAI project:

```bash
bindai new my-project
```

The generated project can then be developed independently while using the BindAI framework.

## Project Scaffolding

The CLI includes templates and scaffolding resources for creating BindAI projects.

A typical workflow is:

```text
bindai new my-project
        │
        ▼
   Project files
        │
        ▼
   Configure project
        │
        ▼
   Add agents / workflows
        │
        ▼
      Develop
```

The package includes its CLI templates and scaffolding resources as package data so they can be distributed with the CLI.

## Development

`bindai-cli` is part of the BindAI workspace.

From the repository root:

```bash
uv sync
```

Run the CLI:

```bash
uv run bindai
```

Run the complete test suite:

```bash
uv run pytest
```

Run static type checking:

```bash
uv run mypy packages/bindai-cli
```

Build the package:

```bash
uv build --package bindai-cli
```

## Package API

The package currently exposes its version through:

```python
from bindai_cli import __version__

print(__version__)
```

Current version:

```text
0.1.8
```

The primary public interface of this package is the command-line application rather than a large Python API.

## Architecture

The CLI sits at the developer-facing edge of the BindAI platform:

```text
Developer
    │
    ▼
BindAI CLI
    │
    ├── Diagnostics
    ├── Inspection
    ├── Initialization
    └── Project Scaffolding
            │
            ▼
       BindAI Project
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
   Agents Workflows Tools
```

This keeps command-line concerns separate from the core BindAI runtime and framework packages.

## Documentation

Full BindAI documentation is available at:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
