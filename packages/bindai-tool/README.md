# BindAI Tool

`bindai-tool` provides the tool abstraction and registration system used by BindAI.

It supports defining tools, wrapping Python functions as tools, registering tools, and representing tool execution results.

## Features

* Tool abstraction
* Tool definitions
* Python function tools
* `tool` decorator
* Tool registry
* Tool execution results
* Reusable tool contracts

## Public API

The package exposes:

```python id="7m3q9x"
from bindai_tool import (
    Tool,
    ToolDefinition,
    FunctionTool,
    ToolRegistry,
    ToolResult,
    tool,
)
```

## Tool

`Tool` is the core abstraction for a BindAI tool.

```python id="4k8n2p"
from bindai_tool import Tool
```

Tools provide a common interface that higher-level BindAI components can use when interacting with executable capabilities.

## ToolDefinition

`ToolDefinition` represents the definition and metadata associated with a tool.

```python id="9v5r1m"
from bindai_tool import ToolDefinition
```

Keeping the tool definition separate from execution allows tools to expose structured information independently of their implementation.

## FunctionTool

`FunctionTool` provides a way to represent a Python function as a BindAI tool.

```python id="2x7c4q"
from bindai_tool import FunctionTool
```

This is useful when existing Python functions need to be exposed through BindAI's tool system.

## Tool Decorator

The `tool` decorator provides a convenient way to define function-based tools.

```python id="6p1n8w"
from bindai_tool import tool


@tool
def calculate_total(a: int, b: int) -> int:
    return a + b
```

The decorator allows ordinary Python functions to participate in the BindAI tool abstraction.

## Tool Registry

`ToolRegistry` manages registered tools.

```python id="3r9m5v"
from bindai_tool import ToolRegistry

registry = ToolRegistry()
```

A registry allows tools to be collected and resolved centrally rather than requiring higher-level components to manage individual tool instances themselves.

## Tool Results

`ToolResult` represents the outcome of tool execution.

```python id="8q2k6x"
from bindai_tool import ToolResult
```

Tool results provide a common result abstraction for communicating the outcome of tool operations to the components that invoked them.

## Architecture

The tool package separates tool definition, implementation, registration, and results:

```text id="5n7w3q"
Python Function
      │
      ▼
 FunctionTool
      │
      ▼
    Tool
      │
      ▼
 ToolRegistry
      │
      ▼
 BindAI Agent / Runtime
      │
      ▼
  ToolResult
```

This allows higher-level BindAI components to work with tools through a consistent abstraction.

## BindAI Integration

`bindai-tool` is a foundational package used by higher-level BindAI components, including agents and execution systems.

It focuses on tool definition, registration, and execution contracts rather than implementing model-provider behavior.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="1m6r8p"
uv sync
```

Run the complete test suite:

```bash id="7x3q9n"
uv run pytest
```

Run static type checking for this package:

```bash id="4c8m2v"
uv run mypy packages/bindai-tool
```

Build the package:

```bash id="9p5k1x"
uv build --package bindai-tool
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
