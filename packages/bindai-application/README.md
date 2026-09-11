# BindAI Application

`bindai-application` provides the application-level abstractions for the BindAI framework.

The package defines the application object and its configuration model, providing a higher-level boundary for applications built on top of the BindAI core infrastructure.

## Public API

The package exposes:

* `Application`
* `ApplicationConfiguration`

```python id="6l5v2c"
from bindai_application import (
    Application,
    ApplicationConfiguration,
)
```

## Application

`Application` represents a BindAI application at the application layer.

It is intended to provide a structured application boundary around the lower-level BindAI framework components.

## Configuration

`ApplicationConfiguration` provides the configuration abstraction associated with a BindAI application.

Keeping application configuration separate from the application object allows configuration to be represented and managed independently.

## Architecture

`bindai-application` sits above the foundational BindAI Core layer:

```text id="x8v3r1"
BindAI Application
        │
        ├── Application
        └── ApplicationConfiguration
                │
                ▼
          bindai-core
```

Higher-level packages can build on these application-level abstractions while sharing the execution and infrastructure provided by `bindai-core`.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="5k3n1p"
uv sync
```

Run the complete test suite:

```bash id="q8r4wd"
uv run pytest
```

Run static type checking for this package:

```bash id="m2x7kc"
uv run mypy packages/bindai-application
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
