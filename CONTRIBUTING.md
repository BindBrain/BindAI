# Contributing to BindAI

Thank you for your interest in contributing to BindAI!

We welcome bug reports, feature requests, documentation improvements, and code contributions from the community.

---

# Development Environment

## Requirements

* Python 3.12+
* Git
* UV (recommended package manager)

Install UV:

```bash
python -m pip install uv
```

Clone the repository:

```bash
git clone https://github.com/BindBrain/BindAI.git
cd BindAI
```

BindAI is organized as a multi-package **uv workspace**.

Install the development workspace:

```bash
uv sync
```

The repository root is a workspace and is not itself installed as an editable package. Do not use `pip install -e .` from the repository root.

---

# Repository Structure

BindAI is organized as a monorepo containing multiple packages.

```text
packages/
    bindai/
    bindai-agent/
    bindai-application/
    bindai-automation/
    bindai-cli/
    bindai-config/
    bindai-core/
    bindai-embeddings/
    bindai-group/
    bindai-host/
    bindai-knowledge/
    bindai-mcp/
    bindai-memory/
    bindai-model/
    bindai-project/
    bindai-prompt-builder/
    bindai-prompts/
    bindai-providers/
    bindai-retrieval/
    bindai-runtime/
    bindai-task/
    bindai-tool/
    bindai-workflow/
    providers/
```

Each package should remain independent whenever practical and should depend on lower-level BindAI abstractions rather than introducing unnecessary coupling.

---

# Coding Guidelines

## Style

* Follow PEP 8.
* Use type hints for new code.
* Prefer dataclasses when appropriate.
* Keep functions focused and small.
* Avoid unnecessary abstractions.
* Preserve existing public APIs unless a change is intentional and documented.
* Follow the architecture and conventions already used by the affected package.

---

## Formatting and Linting

Run Ruff checks from the repository root:

```bash
uv run ruff check .
```

Check formatting without modifying files:

```bash
uv run ruff format --check .
```

If formatting changes are required, apply them with:

```bash
uv run ruff format .
```

---

## Type Checking

Run Pyright:

```bash
uv run pyright
```

Run mypy:

```bash
uv run mypy .
```

When changing typed framework code, address new type-checking errors introduced by the change.

---

# Tests

Run the full test suite:

```bash
uv run pytest
```

Run tests for a specific package:

```bash
uv run pytest packages/bindai-core/tests
```

When changing framework behavior:

* Add regression tests for bugs.
* Add tests for new functionality.
* Keep existing tests passing.
* Prefer focused package tests while developing, followed by the full test suite before submitting a pull request.

---

# Build Packages

Build every package in the workspace:

```bash
uv run python scripts/build_packages.py
```

Package builds should succeed before submitting changes that affect package metadata, packaging, or public APIs.

---

# Documentation

Every new feature should include appropriate documentation.

Documentation lives in:

```text
docs/
```

If you add or change:

* APIs
* builders
* agents
* tools
* workflow nodes
* automation features
* providers
* memory systems
* retrieval systems
* integrations

update the appropriate documentation and examples when necessary.

Examples live in:

```text
examples/
```

Documentation and examples should reflect the actual public API rather than planned or experimental functionality.

---

# Pull Requests

Before opening a Pull Request:

* Ensure all relevant tests pass.
* Run the full test suite.
* Run Ruff checks.
* Check formatting.
* Run type checking when applicable.
* Build packages when packaging or public APIs are affected.
* Update documentation.
* Add tests for new functionality.
* Keep commits focused.
* Use clear commit messages.

Recommended repository checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run mypy .
uv run pytest
uv run python scripts/build_packages.py
```

Not every change requires every check during development, but contributors should run the relevant checks before submitting a pull request.

Use clear commit messages.

Example:

```text
Add workflow timeout policy
```

instead of:

```text
fix stuff
```

---

# Reporting Bugs

When reporting bugs, please include:

* BindAI version
* Python version
* Operating system
* Minimal reproducible example
* Expected behavior
* Actual behavior
* Relevant error output or traceback

Please do not include API keys, passwords, tokens, or other sensitive information in bug reports.

---

# Feature Requests

Feature requests are welcome.

Please explain:

* the problem
* the proposed solution
* potential API design
* example usage
* any relevant compatibility considerations

For larger architectural changes, please discuss the proposed approach before beginning implementation.

---

# Questions

If you're unsure about implementation details, open a GitHub Discussion before starting large changes.

For security vulnerabilities, follow `SECURITY.md` instead of opening a public issue or discussion.

---

# Code of Conduct

By participating in this project, you agree to follow the project's Code of Conduct.
