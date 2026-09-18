# Changelog

All notable changes to BindAI are documented here.

## bindai-cli 0.2.4 — 2026-09-18

This patch release allows `bindai workflow run` to pass command-line arguments to workflow entrypoints.

### Fixed

* `bindai workflow run` now accepts additional arguments after the workflow entrypoint.
* Workflow arguments are forwarded unchanged to the workflow Python process.

### Validation

* Full `bindai-cli` test suite: **68 passed**.
* Ruff validation: **passed**.
* Real demo workflow execution with a prompt: **passed**.

## bindai-cli 0.2.3 — 2026-09-17

This patch release corrects the workflow validation success message so the check mark renders as the intended visible Unicode symbol.

### Fixed

* Replaced the corrupted workflow validation check mark with `✓`.
* Added a regression test covering the visible check mark.

### Validation

* Workflow CLI tests: **passed**.
* Ruff validation: **passed**.
* `bindai-cli` package version is synchronized at `0.2.3`.

## bindai-cli 0.2.2 — 2026-09-17

This patch release corrects `bindai workflow run` so it requires an explicit workflow entrypoint instead of falling back to the project's normal application entrypoint.

### Fixed

* Prevented `bindai workflow run` from launching the project's `main.py` when no workflow path is provided.
* `bindai workflow run` now requires an explicit workflow entrypoint.

### Validation

* Workflow CLI regression test: **passed**.
* Full `bindai-cli` test suite: **65 passed**.
* Ruff validation: **passed**.
* `bindai-cli` package version is synchronized at `0.2.2`.

## bindai-cli 0.2.1 — 2026-09-17

This patch release corrects the CLI's reported version so it matches the published package version.

### Fixed

* Corrected `bindai version` to report `BindAI CLI 0.2.1` instead of the stale `0.1.8` value.

### Validation

* CLI version regression test: **passed**.
* `bindai-cli` package version is synchronized at `0.2.1`.

## bindai 0.1.9 — 2026-09-17

This patch release synchronizes the published `bindai` package README with the current repository documentation and corrects the documentation homepage Quick Start example.

### Changed

* Updated the PyPI package README to match the current `Agent.builder()` API, provider connections, MCP, integrations, package ecosystem, and project documentation.
* Corrected the documentation homepage Quick Start example to use `.instructions()` and `result.output`.
* Advanced `bindai` from `0.1.8` to `0.1.9` for the documentation and packaging correction.

### Validation

* `uv build packages/bindai`: **passed**.
* Both `bindai` 0.1.9 wheel and source distribution passed `twine check`.
* Wheel metadata contains the updated Markdown README.
* Public PyPI `bindai==0.1.9` installation: **passed**.
* Public `bindai` import: **passed**.
* Public `Agent` import: **passed**.

## BindAI 2.0 Milestone — 2026-09-16

This milestone prepares the current BindAI package ecosystem for the next public release line. Package versions remain independently managed rather than being synchronized to a single `2.0.0` PyPI version.

### Package Versions

The distributions included in the initial release publication were:

* `bindai` **0.1.7**
* `bindai-agent` **0.2.0**
* `bindai-cli` **0.2.0**
* `bindai-config` **0.2.0**
* `bindai-connections` **0.2.0**
* `bindai-knowledge` **0.2.0**
* `bindai-memory` **0.1.1**
* `bindai-workflow` **0.2.0**

Other BindAI distributions retain their existing published versions.

### Added

* Project-scoped provider connections.
* Secure OS-backed credential storage through the system keyring.
* Connection manifest metadata for project connections.
* CLI commands for adding, listing, and removing provider connections.
* Configuration support for selecting a named provider connection.
* Connection-aware provider resolution in `AgentBuilder`.
* Connection validation in `bindai doctor`.
* Credential validation for configured connections.
* Restricted workflow expression evaluation and expanded workflow reliability validation.
* Additional configuration and connection regression coverage.

### Changed

* `bindai` advanced from `0.1.6` to `0.1.7` in the initial publication.
* `bindai-agent` advanced from `0.1.2` to `0.2.0`.
* `bindai-cli` advanced from `0.1.8` to `0.2.0`.
* `bindai-config` advanced from `0.1.2` to `0.2.0` in the initial publication.
* `bindai-connections` advanced from `0.1.0` to `0.2.0`.
* `bindai-knowledge` advanced from `0.1.4` to `0.2.0`.
* `bindai-memory` advanced from `0.1.0` to `0.1.1`.
* `bindai-workflow` advanced from `0.1.1` to `0.2.0`.
* Internal dependency minimums were updated to match the new package release line.
* `bindai-cli` now declares the `credentials` extra from `bindai-connections` because the CLI uses the OS-backed credential store.
* `bindai-memory` now declares its PostgreSQL, ChromaDB, and Pinecone runtime dependencies explicitly.
* Package metadata now exposes populated package READMEs for `bindai-memory` and `bindai-knowledge`.
* The release workflow now publishes only the distributions whose versions changed in the initial release.

### Validation

* Full workspace test suite: **160 passed, 2 skipped**.
* Ruff validation: **passed**.
* UV lock consistency: **passed**.
* All 31 workspace packages built successfully.
* 62 distribution artifacts were produced: one wheel and one source distribution for each package.
* All built distributions passed `twine check`.
* Clean installation from built wheels was verified successfully after correcting the `bindai-memory` dependency metadata.
* Connection resolution was verified using an OS keyring credential without an environment API key.
* Connection error paths were verified for unknown connections, provider mismatches, and missing credentials.

## Corrective Dependency Release — 2026-09-16

A fresh public PyPI installation exposed a dependency metadata problem in the initial `bindai` 0.1.7 release: the public `bindai-group` 0.1.0 artifact did not contain the `ParallelProcess` implementation required by the current BindAI package source.

The dependency graph was corrected and republished with:

* `bindai` **0.1.8**
* `bindai-config` **0.2.1**
* `bindai-group` **0.2.0**

### Corrective Changes

* `bindai-group` was advanced to `0.2.0` with the current `ParallelProcess` implementation included.
* `bindai-config` was advanced to `0.2.1` and now requires `bindai-group>=0.2.0`.
* `bindai` was advanced to `0.1.8` and now requires `bindai-config>=0.2.1` and `bindai-group>=0.2.0`.

### Validation

* Corrective distributions passed `twine check`.
* Corrective wheel metadata and package contents were inspected before publication.
* `uv lock --check`: **passed**.
* Ruff validation: **passed**.
* Full workspace test suite: **160 passed, 2 skipped**.
* Fresh public PyPI installation of `bindai==0.1.8`: **passed**.
* Public imports of `bindai`, `bindai_config`, and `bindai_group`: **passed**.
* `ParallelProcess` imported successfully from the public PyPI installation.
* Verified public package versions:
  * `bindai` **0.1.8**
  * `bindai-config` **0.2.1**
  * `bindai-group` **0.2.0**

The corrective release resolves the public dependency mismatch identified after the initial publication.

---

## Previous Releases

Earlier repository tags include historical development, alpha, typed, core-rewrite, and refactoring milestones. They are preserved in Git history but are not reproduced here as formal changelog entries because their historical package contents and release boundaries do not map cleanly to the current BindAI package ecosystem.

For the current development roadmap, see the BindAI documentation.