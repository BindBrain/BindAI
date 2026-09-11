# BindAI Retrieval

`bindai-retrieval` provides retrieval abstractions for the BindAI framework.

The package defines reusable retrieval components, provider contracts, queries, results, and provider registration for applications that need to retrieve relevant information.

## Features

* Retrieval abstraction
* Retriever abstraction
* Retriever provider contract
* Retrieval queries
* Retrieval results
* Provider registry
* Memory-based retrieval provider

## Public API

The package exposes:

```python id="6v3n8q"
from bindai_retrieval import (
    Retrieval,
    Retriever,
    RetrieverProvider,
    RetrievalRegistry,
    RetrievalQuery,
    RetrievalResult,
    MemoryRetrieverProvider,
)
```

## Retrieval

`Retrieval` represents the higher-level retrieval abstraction.

```python id="2m7x4p"
from bindai_retrieval import Retrieval
```

It provides the retrieval layer used by higher-level BindAI components without requiring those components to depend directly on a particular retrieval implementation.

## Retriever

`Retriever` represents the retriever abstraction used to perform retrieval operations.

```python id="8q1k5r"
from bindai_retrieval import Retriever
```

The retriever layer separates retrieval behavior from the underlying provider implementation.

## Retrieval Providers

`RetrieverProvider` defines the provider abstraction behind retrieval implementations.

```python id="4w9c2m"
from bindai_retrieval import RetrieverProvider
```

The package currently exposes `MemoryRetrieverProvider` as a provider implementation:

```python id="7p5n1x"
from bindai_retrieval import MemoryRetrieverProvider
```

This provides a memory-based retrieval implementation suitable for local or in-process retrieval scenarios.

## Retrieval Queries

`RetrievalQuery` represents a retrieval request.

```python id="3r8v6k"
from bindai_retrieval import RetrievalQuery
```

Using a dedicated query abstraction allows retrieval requests to be represented independently of the provider implementation.

## Retrieval Results

`RetrievalResult` represents the result of a retrieval operation.

```python id="9m2q7w"
from bindai_retrieval import RetrievalResult
```

This keeps retrieval results separate from the underlying retrieval provider.

## Retrieval Registry

`RetrievalRegistry` provides registration and lookup for retrieval components.

```python id="5x4n8p"
from bindai_retrieval import RetrievalRegistry
```

A registry allows retrieval providers and related components to be resolved through a common mechanism.

## Architecture

The retrieval package provides a provider-based retrieval layer:

```text id="1k6r9v"
Application / Agent
        │
        ▼
    Retrieval
        │
        ▼
     Retriever
        │
        ▼
 RetrieverProvider
        │
        ▼
MemoryRetrieverProvider
```

Queries and results provide the data contracts around retrieval operations.

## BindAI Integration

`bindai-retrieval` is designed to sit between higher-level BindAI components and retrieval implementations.

It can be used alongside the knowledge and memory layers while keeping retrieval concerns separated from application and agent execution.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="7n3m5x"
uv sync
```

Run the complete test suite:

```bash id="4q8v1p"
uv run pytest
```

Run static type checking for this package:

```bash id="6m2r9k"
uv run mypy packages/bindai-retrieval
```

Build the package:

```bash id="8x5c3n"
uv build --package bindai-retrieval
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
