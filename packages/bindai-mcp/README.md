# BindAI MCP

`bindai-mcp` provides MCP integration functionality for connecting BindAI applications and agents to external tool services.

The package exposes a small public API centered around `MCPClient` and `MCPTool`.

> **Current status:** The package currently provides a lightweight HTTP-based tool discovery and invocation bridge. Full Model Context Protocol interoperability is part of the BindAI MCP roadmap.

## Features

* MCP integration foundation
* Remote tool discovery
* Representation of discovered tools as BindAI tools
* Integration of external tools into BindAI applications
* Lightweight public Python API
* Separation between MCP integration and BindAI core functionality

## Installation

`bindai-mcp` is part of the BindAI workspace.

From the BindAI repository root:

```bash
uv sync
```

The package can then be used through the workspace environment.

For public package installation, install the published `bindai-mcp` package from PyPI when the corresponding release is available.

## Basic Usage

The public API can be imported as:

```python
from bindai_mcp import MCPClient, MCPTool
```

`MCPClient` provides the client-side integration, while `MCPTool` represents a remotely exposed tool as a BindAI tool.

The current implementation uses an HTTP service exposing tool discovery and invocation endpoints.

A typical integration flow is:

```text
BindAI Agent / Application
           │
           ▼
       MCPClient
           │
           ▼
     HTTP Tool Service
           │
      ┌────┴────┐
      ▼         ▼
   Tool A     Tool B
```

The current client expects:

```text
GET  /tools
POST /call
```

The exact request and response behavior is provided by the package implementation.

## Public API

### MCPClient

`MCPClient` is the primary client interface for discovering external tools.

```python
from bindai_mcp import MCPClient
```

Example:

```python
client = MCPClient("http://localhost:8000")
tools = await client.list_tools()
```

### MCPTool

`MCPTool` represents a remotely available tool using BindAI's tool abstraction.

```python
from bindai_mcp import MCPTool
```

Discovered tools can be represented as BindAI tools and integrated with BindAI agent execution.

## BindAI Integration

The MCP integration keeps external tool connectivity separate from BindAI's core execution and agent abstractions.

Conceptually:

```text
                 BindAI
                    │
           ┌────────┴────────┐
           │                 │
         Agent          Application
           │                 │
           └────────┬────────┘
                    │
                MCPClient
                    │
                    ▼
             External Tool
               Service
                    │
              ┌─────┴─────┐
              ▼           ▼
           MCPTool     MCPTool
```

This separation allows the MCP integration layer to evolve independently from the BindAI core framework.

## MCP Roadmap

The BindAI MCP package is intended to evolve toward full MCP protocol support.

Planned capabilities include:

* Standard MCP client communication
* MCP tool discovery
* MCP tool invocation
* MCP resource support where appropriate
* BindAI agent integration
* Authentication and configuration
* MCP server integration where appropriate
* Documentation and examples
* Protocol-level interoperability testing

The current HTTP tool bridge should therefore be considered the foundation for the broader MCP integration rather than a complete MCP protocol implementation.

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
├── src/
│   └── bindai_mcp/
│       ├── __init__.py
│       └── client.py
└── tests/
    └── test_client.py
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
