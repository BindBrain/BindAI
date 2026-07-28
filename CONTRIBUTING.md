# Contributing to BindAI

Thank you for your interest in contributing to BindAI!

We welcome bug reports, feature requests, documentation improvements, and code contributions from the community.

---

# Development Environment

## Requirements

- Python 3.11+
- Git
- UV (recommended package manager)

Install UV:

```bash
pip install uv
```

Clone the repository:

```bash
git clone https://github.com/BindBrain/BindAI.git
cd BindAI
```

Install dependencies:

```bash
uv sync
```

---

# Repository Structure

BindAI is organized as a monorepo containing multiple packages.

```
packages/
    bindai/
    bindai-core/
    bindai-agent/
    bindai-workflow/
    bindai-memory/
    bindai-knowledge/
    bindai-model/
    bindai-tool/
    ...
```

Each package should remain independent whenever possible.

---

# Coding Guidelines

## Style

- Follow PEP 8.
- Use type hints everywhere.
- Prefer dataclasses when appropriate.
- Keep functions focused and small.
- Avoid unnecessary abstractions.

---

## Formatting

Before submitting a Pull Request, run:

```bash
ruff check .
ruff format .
```

---

## Type Checking

```bash
pyright
```

---

## Tests

Run all tests:

```bash
pytest
```

Run a specific package:

```bash
pytest packages/bindai-core/tests
```

---

# Documentation

Every new feature should include documentation.

Documentation lives in:

```
docs/
```

If you add:

- new APIs
- builders
- workflow nodes
- providers
- memory systems

please update the appropriate documentation page.

---

# Pull Requests

Before opening a Pull Request:

- Ensure all tests pass.
- Update documentation.
- Add tests for new functionality.
- Keep commits focused.
- Use clear commit messages.

Example:

```
Add workflow timeout policy
```

instead of

```
fix stuff
```

---

# Reporting Bugs

When reporting bugs, please include:

- BindAI version
- Python version
- Operating system
- Minimal reproducible example
- Expected behavior
- Actual behavior

---

# Feature Requests

Feature requests are welcome.

Please explain:

- the problem
- the proposed solution
- potential API design
- example usage

---

# Questions

If you're unsure about implementation details, open a GitHub Discussion before starting large changes.

---

# Code of Conduct

By participating in this project, you agree to follow the project's Code of Conduct.