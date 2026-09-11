# BindAI MCP

`bindai-mcp` provides Model Context Protocol (MCP) client functionality for connecting BindAI applications and agents to MCP-compatible tools and services.

The package exposes a small public API centered around `MCPClient` and `MCPTool`.

## Features

* MCP client connectivity
* MCP tool discovery and representation
* Integration of MCP tools into BindAI applications
* Lightweight public Python API
* Separation between MCP integration and BindAI core functionality

## Installation

`bindai-mcp` is part of the BindAI workspace.

From the BindAI repository root:

```bash
uv sync
```

The package can then be used through the workspace environment.

## Basic Usage

The public API can be imported as:

```python
from bindai_mcp import MCPClient, MCPTool
```

`MCPClient` provides the client-side MCP integration, while `MCPTool` represents an MCP tool exposed through the integration.

A typical integration has the following conceptual flow:

```text
BindAI Agent / Application
          │
          ▼
      MCPClient
          │
          ▼
    MCP-compatible
       Server
          │
          ▼
       MCPTool
```

The exact connection and tool invocation behavior is provided by the package implementation.

## Public API

### MCPClient

`MCPClient` is the primary client interface for connecting BindAI code to MCP-compatible services.

```python
from bindai_mcp import MCPClient
```

### MCPTool

`MCPTool` represents an MCP tool that can be discovered or used through an MCP connection.

```python
from bindai_mcp import MCPTool
```

## BindAI Integration

MCP integration allows BindAI applications to work with tools exposed outside the core framework.

Conceptually:

```text
                 BindAI
                    │
             ┌──────┴──────┐
             │             │
           Agent        Application
             │             │
             └──────┬──────┘
                    │
                MCPClient
                    │
                    ▼
              MCP Server
                    │
              ┌─────┴─────┐
              ▼           ▼
           MCPTool     MCPTool
```

This keeps MCP-specific functionality isolated from the core BindAI execution and agent abstractions.

## Development

From the repository root:

```bash
uv sync
```

Run the complete test suite:

```bash
uv run pytest
```

Run type checking for the package:

```bash
uv run mypy packages/bindai-mcp
```

Build the package:

```bash
uv build --package bindai-mcp
```

## Package Structure

The package follows the standard BindAI package layout:

```text
bindai-mcp/
├── pyproject.toml
├── README.md
└── src/
    └── bindai_mcp/
        ├── __init__.py
        └── client.py
```

## API Stability

The package currently exposes:

```python
from bindai_mcp import MCPClient, MCPTool
```

These are the intended public entry points of the package.

Internal implementation details should be treated as subject to change unless explicitly documented as public API.

## Documentation

Full BindAI documentation is available at:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
