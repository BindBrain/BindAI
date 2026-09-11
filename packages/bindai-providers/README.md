# BindAI Providers

`bindai-providers` provides the provider infrastructure used by BindAI to configure, construct, register, and bootstrap model providers.

The package builds on the provider contracts defined by `bindai-core` and provides higher-level provider management through `ProviderBuilder`, `ProviderRegistry`, and `bootstrap`.

## Features

* Model provider infrastructure
* Provider configuration
* Provider capabilities
* Provider factories
* Provider registry
* Provider builder
* Provider bootstrap
* Model request and response contracts
* Streaming response support
* Token usage information

Provider implementations are maintained separately from this package.

## Public API

The package exposes the following provider contracts and utilities:

```python id="l0d5qj"
from bindai_providers import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ProviderCapabilities,
    ProviderConfiguration,
    ProviderFactory,
    ProviderRegistry,
    StreamChunk,
    TokenUsage,
    ProviderBuilder,
    bootstrap,
)
```

### ModelProvider

The `ModelProvider` contract represents a model provider capable of processing BindAI model requests.

```python id="x3o4ai"
from bindai_providers import ModelProvider
```

Provider implementations can conform to this abstraction without requiring BindAI applications to depend directly on a specific provider implementation.

### ModelRequest

`ModelRequest` represents a request sent to a model provider.

```python id="h0n4hz"
from bindai_providers import ModelRequest
```

### ModelResponse

`ModelResponse` represents a provider response.

```python id="q2j5pj"
from bindai_providers import ModelResponse
```

### ProviderCapabilities

`ProviderCapabilities` describes the capabilities supported by a provider.

```python id="c9n4rd"
from bindai_providers import ProviderCapabilities
```

### ProviderConfiguration

`ProviderConfiguration` represents provider configuration information.

```python id="u4c0k8"
from bindai_providers import ProviderConfiguration
```

### ProviderFactory

`ProviderFactory` provides the factory abstraction used to construct providers.

```python id="6h3t7p"
from bindai_providers import ProviderFactory
```

### ProviderRegistry

`ProviderRegistry` manages registered providers.

```python id="m9e5qs"
from bindai_providers import ProviderRegistry
```

### ProviderBuilder

`ProviderBuilder` provides a higher-level interface for configuring and constructing providers.

```python id="f2d7nw"
from bindai_providers import ProviderBuilder
```

### StreamChunk

`StreamChunk` represents an incremental streaming response from a provider.

```python id="w8p3kv"
from bindai_providers import StreamChunk
```

### TokenUsage

`TokenUsage` represents token usage information associated with a model request.

```python id="a6r1ze"
from bindai_providers import TokenUsage
```

### bootstrap

`bootstrap` initializes the provider infrastructure.

```python id="k5s9xb"
from bindai_providers import bootstrap

bootstrap()
```

## Provider Architecture

The provider package sits between BindAI's core provider contracts and concrete provider implementations:

```text id="f3j8mw"
                 BindAI Application
                        │
                        ▼
                 ProviderBuilder
                        │
                        ▼
                 ProviderRegistry
                        │
                        ▼
                 ProviderFactory
                        │
                        ▼
                  ModelProvider
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       OpenAI       Anthropic       Google
       Provider      Provider       Provider
```

Concrete providers remain separate packages. This allows the core provider infrastructure to remain independent from individual model vendors.

## Requests and Responses

BindAI provider interactions use shared contracts:

```text id="q7x2cb"
ModelRequest
     │
     ▼
ModelProvider
     │
     ├── ModelResponse
     │
     └── StreamChunk
             │
             ▼
         TokenUsage
```

This provides a consistent interface for synchronous and streaming model interactions.

## Provider Registration

Providers can be managed through `ProviderRegistry`:

```python id="r4v1hs"
from bindai_providers import ProviderRegistry

registry = ProviderRegistry()
```

The registry provides the central provider lookup mechanism used by the provider infrastructure.

## Provider Construction

`ProviderBuilder` provides a higher-level construction API:

```python id="b8k2mf"
from bindai_providers import ProviderBuilder

builder = ProviderBuilder()
```

The builder is intended to keep provider configuration and construction separate from application code.

## Development

From the BindAI repository root:

```bash id="j5t6qa"
uv sync
```

Run the complete test suite:

```bash id="n1z8sc"
uv run pytest
```

Run type checking:

```bash id="e4p7yd"
uv run mypy packages/bindai-providers
```

Build the package:

```bash id="k6m2zr"
uv build --package bindai-providers
```

## Package Structure

```text id="u8w4hf"
bindai-providers/
├── pyproject.toml
├── README.md
└── src/
    └── bindai_providers/
        ├── __init__.py
        ├── bootstrap.py
        ├── builder.py
        └── registry.py
```

## Provider Implementations

Concrete provider packages are maintained independently, including integrations for supported model providers.

This package intentionally focuses on shared provider infrastructure rather than vendor-specific API implementations.

## Documentation

Full BindAI documentation is available at:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
