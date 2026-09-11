# BindAI Memory

`bindai-memory` provides memory abstractions and storage providers for the BindAI framework.

It provides a common memory API that allows applications and agents to store and retrieve memory records while supporting multiple provider implementations.

## Features

* Memory abstractions
* Memory records and memory types
* Memory management
* Provider abstraction
* Provider registry
* In-memory storage
* SQLite storage
* Vector-based storage
* Memory results

## Public API

The package exposes the main memory components directly from `bindai_memory`:

```python id="4r7k2m"
from bindai_memory import (
    Memory,
    MemoryManager,
    MemoryProvider,
    MemoryRecord,
    MemoryRegistry,
    MemoryResult,
    MemoryType,
)
```

Provider implementations include:

```python id="8p3n6v"
from bindai_memory import (
    InMemoryProvider,
    SQLiteMemoryProvider,
    VectorMemoryProvider,
)
```

## Memory Providers

`MemoryProvider` defines the common provider abstraction used by memory implementations.

BindAI Memory currently provides:

* `InMemoryProvider`
* `SQLiteMemoryProvider`
* `VectorMemoryProvider`

This allows the memory layer to use different storage strategies behind a common provider interface.

## Memory Registry

`MemoryRegistry` provides provider registration and lookup.

The package registers the in-memory provider under the `in_memory` key during package initialization.

```python id="6w2c9q"
from bindai_memory import MemoryRegistry

provider = MemoryRegistry.get("in_memory")
```

Provider registration allows memory implementations to be resolved through a common registry rather than coupling applications to a specific provider class.

## Memory Records

`MemoryRecord` represents an individual memory entry, while `MemoryType` identifies the type of memory.

```python id="1v5m8s"
from bindai_memory import (
    MemoryRecord,
    MemoryType,
)
```

`MemoryResult` provides the result abstraction returned by memory operations.

## Memory Manager

`MemoryManager` provides the higher-level management layer for memory operations.

```python id="9k4p2x"
from bindai_memory import MemoryManager

manager = MemoryManager()
```

The exact provider configuration depends on the selected memory implementation.

## Architecture

The memory package is structured around a provider abstraction:

```text id="5n8q3r"
Application / Agent
        │
        ▼
  MemoryManager
        │
        ▼
   MemoryProvider
        │
   ┌────┼──────────────┐
   │    │              │
   ▼    ▼              ▼
InMemory  SQLite      Vector
Provider  Provider    Provider
```

This separation allows the higher-level memory API to remain independent of the underlying storage implementation.

## BindAI Integration

`bindai-memory` integrates with the broader BindAI framework through its core and embedding abstractions.

It can be used by higher-level components such as agents while keeping memory storage concerns separate from agent execution logic.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="3x6m1q"
uv sync
```

Run the complete test suite:

```bash id="7p2r8c"
uv run pytest
```

Run static type checking for this package:

```bash id="5k9v2n"
uv run mypy packages/bindai-memory
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
