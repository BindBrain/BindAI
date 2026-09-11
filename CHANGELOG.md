# Changelog

All notable changes to BindAI are documented here.

## v0.1.5 — 2026-09-08

### Added

* `Agent.builder()` as the recommended agent construction API.
* Agent delegation and team-oriented execution patterns.
* Agent groups and parallel multi-agent execution.
* Advanced tool execution.
* Selected role-chain execution for multi-agent workflows.
* Connections and integration infrastructure.
* Connection manager and connection registry.
* Webhook integration.
* GitHub integration.
* Slack integration.
* Notion integration.
* Jira integration.
* Discord integration.
* Resend integration.
* Vercel integration.
* Netlify integration.
* MCP client support for tool discovery and execution.
* Expanded Knowledge and RAG capabilities.
* Conversational retrieval support.
* Retrieval and reranking improvements.
* Expanded provider ecosystem with OpenAI, Anthropic, Google Gemini, Groq, Ollama, and OpenRouter support.
* Automation definitions and execution infrastructure.
* Event trigger framework.
* Unified trigger management.
* Automation execution state and state-store abstractions.
* Automation run history and history-store abstractions.
* Background automation workers.
* Expanded documentation covering agents, tools, memory, knowledge, workflows, projects, connections, automation, and API reference.
* Updated roadmap and package documentation.
* Release metadata and workspace improvements for the BindAI package ecosystem.

### Changed

* `bindai` now requires `bindai-agent>=0.1.2`.
* `bindai` version advanced to `0.1.5`.
* `bindai-agent` version advanced to `0.1.2`.
* Google and Groq provider packages were added to the UV workspace configuration.
* Workspace lock metadata was updated to include the complete current provider package set.
* Documentation was aligned with the current public APIs and implemented capabilities.
* The automation layer was extended from trigger infrastructure into execution tracking, historical run records, and background execution.

### Validation

* Full workspace test suite: **160 passed, 2 skipped**.
* Agent package tests: **31 passed**.
* Automation package tests: **52 passed**.
* Multi-agent group tests pass for sequential and parallel execution.
* BindAI and BindAI Agent wheels build successfully.
* Built distributions pass `twine check`.
* Local wheel installation verified `Agent.builder()` successfully.

### Notes

This release represents the current BindAI development line and provides a substantial foundation for a future public open-source release.

The framework now includes agents, tools, workflows, memory, Knowledge and RAG, multiple model providers, connections, MCP support, multi-agent execution, and an automation foundation with triggers, execution state, run history, and background workers.

Some roadmap areas remain under active development, including advanced event routing, planning and more advanced multi-agent coordination, deployment, observability, visual workflow tooling, and other future platform capabilities.

---

## Previous Releases

Earlier repository tags include historical development, alpha, typed, core-rewrite, and refactoring milestones. They are preserved in Git history but are not reproduced here as formal changelog entries because their historical package contents and release boundaries do not map cleanly to the current BindAI package ecosystem.

For the current development roadmap, see the BindAI documentation.
