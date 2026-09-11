# BindAI Core

`bindai-core` provides the foundational kernel and contracts used throughout the BindAI framework.

It contains the low-level abstractions for execution, context, events, runtime infrastructure, model and provider contracts, prompts, conversations, resources, registries, middleware, and application infrastructure.

The package is designed to provide reusable framework infrastructure rather than concrete AI-provider implementations.

## Core Responsibilities

### Execution

BindAI Core defines the common execution contracts used by higher-level components:

* `Executable`
* `ExecutionResult`
* `ExecutionStatus`
* `ExecutionError`
* `ExecutionRequest`
* `ExecutionResponse`

These contracts provide a consistent foundation for executing BindAI components.

### Execution Context

Core provides the context and state objects used during execution:

* `ExecutionContext`
* `ExecutionState`
* `Variables`

These abstractions allow execution data and variables to be passed through framework components.

### Events

The event system provides framework-level event infrastructure:

* `Event`
* `EventBus`
* `EventTypes`

Higher-level BindAI packages can use these primitives to publish and consume framework events.

### Runtime

Core exposes runtime infrastructure including:

* `BindRuntime`
* `RuntimeOptions`
* `RuntimeState`
* `ExecutionPipeline`

This provides the foundation for coordinating execution within the BindAI runtime.

### Model and Provider Contracts

Core defines common interfaces and data structures for models and providers:

* `ModelProvider`
* `ModelRequest`
* `ModelResponse`
* `ProviderCapabilities`
* `Message`
* `MessageRole`
* `TokenUsage`
* `StreamChunk`
* `ToolCall`
* `ProviderConfiguration`
* `ProviderFactory`
* `ProviderRegistry`

Concrete provider implementations are supplied by separate BindAI provider packages.

### Prompts and Conversations

Core provides reusable prompt and conversation abstractions:

* `Prompt`
* `PromptBuilder`
* `PromptTemplate`
* `Conversation`
* `ConversationMessage`

These components are used by higher-level packages such as the BindAI agent layer.

### Framework Infrastructure

Core also provides general framework infrastructure:

* `Bind`
* `BindApplication`
* `BindContainer`
* `ServiceLifetime`
* `Registry`
* `Resource`
* `Middleware`
* `EmbeddingProvider`

## Architecture

`bindai-core` sits at the foundation of the BindAI package ecosystem.

```text
BindAI Applications
        │
        ├── Agents
        ├── Workflows
        ├── Groups
        ├── Automation
        └── Other BindAI Components
                │
                ▼
          bindai-core
                │
                ├── Execution
                ├── Context
                ├── Events
                ├── Runtime
                ├── Model Contracts
                ├── Provider Contracts
                ├── Prompts
                ├── Conversations
                ├── Registries
                └── Framework Infrastructure
```

Higher-level BindAI packages build on these shared contracts rather than reimplementing foundational execution and framework behavior.

## No Provider Implementations

`bindai-core` does **not** contain concrete AI-provider implementations.

Provider integrations such as OpenAI, Anthropic, Google, Groq, Ollama, and OpenRouter are maintained in separate packages.

This keeps the core package independent from individual AI service implementations.

## Public API

The main public exports are available directly from `bindai_core`:

```python
from bindai_core import (
    ExecutionContext,
    ExecutionResult,
    Executable,
    Event,
    EventBus,
    ModelRequest,
    ModelResponse,
    ProviderRegistry,
    Prompt,
    Conversation,
    Registry,
)
```

The complete public surface is defined by the package's `bindai_core.__all__` export list.

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

Run static type checking:

```bash
uv run mypy packages/bindai-core
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
