# BindAI Model

`bindai-model` provides the model abstraction layer for BindAI.

It defines the common interfaces and result types used to work with AI models, together with model provider registration and provider implementations.

## Features

* Model abstraction
* Model provider abstraction
* Model results
* Model provider registry
* OpenAI model provider
* Provider registration through `ModelRegistry`

## Public API

The main components are available directly from `bindai_model`:

```python
from bindai_model import (
    Model,
    ModelProvider,
    ModelRegistry,
    ModelResult,
    OpenAIProvider,
)
```

## Model Abstraction

`Model` represents the higher-level model abstraction used by BindAI.

`ModelProvider` defines the provider contract behind model execution.

```text
Model
  │
  ▼
ModelProvider
  │
  └── Provider implementation
```

This separation keeps model-facing functionality independent from a specific provider implementation.

## Model Registry

`ModelRegistry` provides provider registration and lookup.

The package registers the OpenAI provider under the `openai` key:

```python
from bindai_model import ModelRegistry

provider = ModelRegistry.get("openai")
```

Provider registration allows higher-level BindAI components to resolve providers through a common registry.

## OpenAI Provider

The package currently exposes `OpenAIProvider` as its model provider implementation.

```python
from bindai_model import OpenAIProvider
```

The provider is registered automatically when the package is initialized.

## Model Results

`ModelResult` represents the result produced by model operations.

```python
from bindai_model import ModelResult
```

Using a dedicated result type keeps model execution results separate from provider-specific implementation details.

## Architecture

The model package sits between higher-level BindAI components and model-provider implementations:

```text
BindAI Agent / Application
          │
          ▼
        Model
          │
          ▼
    ModelProvider
          │
          ▼
   Model Provider
```

The registry provides provider discovery and registration across the model layer.

## BindAI Integration

`bindai-model` is a foundational package used by higher-level BindAI components that need model abstractions.

Provider-specific integrations remain separate from the core model contracts where possible.

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
uv run mypy packages/bindai-model
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
