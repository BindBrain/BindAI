# Changelog

All notable changes to BindAI are documented here.

## BindAI 2.0 Milestone — 2026-09-16

This milestone prepares the current BindAI package ecosystem for the next public release line. Package versions remain independently managed rather than being synchronized to a single `2.0.0` PyPI version.

### Package Versions

The distributions included in this release are:

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

* `bindai` advanced from `0.1.6` to `0.1.7`.
* `bindai-agent` advanced from `0.1.2` to `0.2.0`.
* `bindai-cli` advanced from `0.1.8` to `0.2.0`.
* `bindai-config` advanced from `0.1.2` to `0.2.0`.
* `bindai-connections` advanced from `0.1.0` to `0.2.0`.
* `bindai-knowledge` advanced from `0.1.4` to `0.2.0`.
* `bindai-memory` advanced from `0.1.0` to `0.1.1`.
* `bindai-workflow` advanced from `0.1.1` to `0.2.0`.
* Internal dependency minimums were updated to match the new package release line.
* `bindai-cli` now declares the `credentials` extra from `bindai-connections` because the CLI uses the OS-backed credential store.
* `bindai-memory` now declares its PostgreSQL, ChromaDB, and Pinecone runtime dependencies explicitly.
* Package metadata now exposes populated package READMEs for `bindai-memory` and `bindai-knowledge`.
* The release workflow now publishes only the distributions whose versions changed in this release.

### Validation

* Full workspace test suite: **160 passed, 2 skipped**.
* Ruff validation: **passed**.
* UV lock consistency: **passed**.
* All 31 workspace packages built successfully.
* 62 distribution artifacts were produced: one wheel and one source distribution for each package.
* All built distributions passed `twine check`.
* Clean installation from built wheels was previously verified successfully after correcting the `bindai-memory` dependency metadata.
* Connection resolution was verified using an OS keyring credential without an environment API key.
* Connection error paths were verified for unknown connections, provider mismatches, and missing credentials.

### Notes

This milestone represents a package-ecosystem release point rather than a synchronized `2.0.0` version across every distribution.

Only packages whose metadata or implementation changed are being republished. Packages that did not change retain their existing PyPI versions.

The documentation roadmap will be updated after the PyPI publication and final release verification so that the public documentation reflects the actual published state.

---

## Previous Releases

Earlier repository tags include historical development, alpha, typed, core-rewrite, and refactoring milestones. They are preserved in Git history but are not reproduced here as formal changelog entries because their historical package contents and release boundaries do not map cleanly to the current BindAI package ecosystem.

For the current development roadmap, see the BindAI documentation.
