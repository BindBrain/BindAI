# BindAI Prompts

`bindai-prompts` provides reusable prompt abstractions for the BindAI framework.

The package defines prompts, prompt templates, and a prompt registry so prompt definitions can be organized and reused across BindAI applications and components.

## Features

* Prompt abstraction
* Prompt templates
* Prompt registry
* Reusable prompt definitions
* Centralized prompt registration

## Public API

The package exposes:

```python id="4m7q2x"
from bindai_prompts import (
    Prompt,
    PromptTemplate,
    PromptRegistry,
)
```

## Prompt

`Prompt` represents a prompt within the BindAI prompt layer.

```python id="8k3v1p"
from bindai_prompts import Prompt
```

Prompts provide a reusable abstraction that can be consumed by higher-level BindAI components.

## PromptTemplate

`PromptTemplate` provides a reusable template abstraction for prompt construction.

```python id="2w9n5c"
from bindai_prompts import PromptTemplate
```

Templates allow prompt definitions to be separated from the code that consumes them.

## Prompt Registry

`PromptRegistry` provides a registry for managing prompt definitions.

```python id="6r1x8m"
from bindai_prompts import PromptRegistry
```

A registry allows prompts to be organized and resolved by name or identifier rather than requiring every consumer to construct or import prompts directly.

## Architecture

The prompts package provides the reusable prompt-definition layer:

```text id="9p4t6y"
Prompt Definitions
       │
       ├── Prompt
       │
       └── PromptTemplate
              │
              ▼
       PromptRegistry
              │
              ▼
    BindAI Applications
    / Agents / Components
```

Prompt construction utilities in `bindai-prompt-builder` can build on these prompt abstractions when applications need contextual prompt construction.

## BindAI Integration

`bindai-prompts` focuses on reusable prompt definitions.

It does not perform model-provider execution. Model execution remains the responsibility of the appropriate BindAI model and agent layers.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="3n8w5k"
uv sync
```

Run the complete test suite:

```bash id="7c2m9q"
uv run pytest
```

Run static type checking for this package:

```bash id="5x1r8v"
uv run mypy packages/bindai-prompts
```

Build the package:

```bash id="4q6k2z"
uv build --package bindai-prompts
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
