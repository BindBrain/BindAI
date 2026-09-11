# BindAI Knowledge

`bindai-knowledge` provides knowledge and retrieval building blocks for the BindAI framework.

It provides abstractions for loading documents, splitting them into chunks, generating embeddings, storing knowledge, searching, reranking results, and building knowledge pipelines.

## Features

* Knowledge collections
* Knowledge documents and chunks
* Document loaders
* Document chunking
* Embedding support
* Knowledge providers
* Knowledge search options
* Result reranking
* Knowledge pipelines
* Conversation-aware queries
* In-memory knowledge storage
* JSON-backed knowledge storage
* Vector knowledge providers
* Fake and dummy embedding providers

## Public API

The package exposes the main knowledge abstractions directly from `bindai_knowledge`:

```python id="7m4q2k"
from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
    KnowledgeChunk,
    KnowledgeProvider,
    KnowledgeResult,
    KnowledgeSearchOptions,
    KnowledgePipeline,
)
```

## Document Loading

BindAI Knowledge provides loaders for several document sources:

* `TextLoader`
* `MarkdownLoader`
* `PDFLoader`
* `HTMLLoader`
* `DirectoryLoader`

The common loader contract is provided by `DocumentLoader`.

```python id="5v8n1c"
from bindai_knowledge import (
    DocumentLoader,
    TextLoader,
)

loader = TextLoader()
```

Specific loader behavior depends on the loader implementation and its input requirements.

## Document Chunking

Documents can be divided into knowledge chunks using the provided chunkers:

* `DocumentChunker`
* `FixedChunker`
* `RecursiveChunker`

These components provide the preprocessing layer used before embedding and knowledge storage.

## Embeddings

The package integrates with the BindAI embedding abstraction:

```python id="2p6x9r"
from bindai_knowledge import EmbeddingProvider

# Implementations can provide embeddings for knowledge documents.
```

Development and testing implementations include:

* `FakeEmbeddingProvider`
* `DummyEmbeddingProvider`

## Knowledge Providers

The `KnowledgeProvider` abstraction defines the provider boundary for knowledge storage and retrieval.

Available implementations include:

* `InMemoryKnowledgeProvider`
* `JsonKnowledgeProvider`
* `VectorKnowledgeProvider`

This allows applications to use different storage strategies without changing the higher-level knowledge abstractions.

## Search and Reranking

Knowledge search can be configured using `KnowledgeSearchOptions`.

The package also provides reranking abstractions and a lexical implementation:

* `Reranker`
* `LexicalReranker`

## Knowledge Pipeline

`KnowledgePipeline` provides a higher-level abstraction for composing knowledge-processing operations.

The package also provides `ConversationQuery` for knowledge queries that incorporate conversational context.

## Architecture

The knowledge layer can be viewed conceptually as:

```text
Documents
   │
   ▼
Document Loaders
   │
   ▼
Chunking
   │
   ▼
Embeddings
   │
   ▼
Knowledge Provider
   │
   ▼
Search
   │
   ▼
Reranking
   │
   ▼
Knowledge Results
```

BindAI Knowledge provides the components at each stage while allowing implementations to be selected independently.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="4t7w2m"
uv sync
```

Run the complete test suite:

```bash id="8c3p5n"
uv run pytest
```

Run static type checking for this package:

```bash id="6r1k9v"
uv run mypy packages/bindai-knowledge
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
