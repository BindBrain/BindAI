# BindAI Prompt Builder

`bindai-prompt-builder` provides prompt-building utilities for BindAI applications.

It separates prompt construction from application and agent execution, providing a reusable prompt builder and build context.

## Features

* Prompt construction
* Prompt build context
* Reusable prompt-building utilities
* Separation between prompt construction and execution

## Public API

The package exposes:

```python id="2k7v4n"
from bindai_prompt_builder import (
    PromptBuilder,
    PromptBuildContext,
)
```

## PromptBuilder

`PromptBuilder` is the primary public utility for constructing prompts.

```python id="8r3m1x"
from bindai_prompt_builder import PromptBuilder

builder = PromptBuilder()
```

The builder can be used by higher-level BindAI components to construct prompts without coupling prompt construction directly to model or agent execution.

## PromptBuildContext

`PromptBuildContext` represents the context available while building a prompt.

```python id="6t9q2p"
from bindai_prompt_builder import PromptBuildContext
```

Keeping the build context separate from the builder allows prompt construction to receive contextual information without embedding that responsibility into the prompt builder itself.

## Architecture

The prompt-builder package belongs to the prompt construction layer:

```text id="3m8w6q"
Application / Agent
        │
        ▼
  PromptBuilder
        │
        ▼
PromptBuildContext
        │
        ▼
     Prompt
```

The resulting prompt can then be consumed by the appropriate higher-level BindAI component.

## BindAI Integration

`bindai-prompt-builder` is designed to be reusable across BindAI applications and components that need structured prompt construction.

It focuses on prompt-building concerns rather than model-provider execution.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="5q2j8c"
uv sync
```

Run the complete test suite:

```bash id="7m4p1v"
uv run pytest
```

Run static type checking for this package:

```bash id="9x6n3k"
uv run mypy packages/bindai-prompt-builder
```

Build the package:

```bash id="1c8r5w"
uv build --package bindai-prompt-builder
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
