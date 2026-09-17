# BindAI Roadmap

BindAI is being built as a complete open-source platform for developing, deploying, automating, and operating AI applications.

The roadmap below describes the major capabilities of BindAI and the progression from its core AI application framework toward a broader AI automation and enterprise platform.

> The roadmap represents our direction and priorities. Features and priorities may evolve as the framework develops and as we learn from the community.

## Status markers

- `[x]` Completed
- `[~]` Partially implemented
- `[ ]` Planned / remaining

---

# Current — v0.1 Foundation

## AI Application Foundation

The core application foundation of BindAI is implemented and forms the base of the public framework.

### Completed

- [x] AI agents
- [x] Tools and tool calling
- [x] Memory and context
- [x] Knowledge and RAG integration
- [x] Workflow orchestration
- [x] Conditional execution
- [x] Loops
- [x] Parallel execution
- [x] Retries and timeouts
- [x] Human approval and tasks
- [x] Scheduling
- [x] Projects
- [x] CLI tooling
- [x] Modular package architecture
- [x] Workflow templates
- [x] Agent delegation
- [x] Team delegation
- [x] Specialist role chains
- [x] Agent hooks, callbacks, and middleware
- [x] Agent execution configuration
- [x] Conversation management
- [x] Tool registry and execution
- [x] Structured execution context
- [x] Runtime and application configuration
- [x] Package-based framework architecture
- [x] Documentation and automated testing

The foundation provides a modular Python architecture that developers can extend without being locked into a single AI provider or execution model.

---

# Current — Provider Ecosystem

## AI Providers

BindAI provides a provider abstraction and registry for working with multiple AI model providers.

### Completed

- [x] OpenAI
- [x] Anthropic
- [x] Google Gemini
- [x] Ollama
- [x] OpenRouter
- [x] Groq
- [x] Provider registry
- [x] Provider bootstrap architecture
- [x] Consistent provider interfaces
- [x] CLI provider initialization

### Remaining

- [ ] Azure OpenAI
- [ ] Mistral
- [ ] Additional compatible providers

Applications should be able to switch providers and models without changing their core application architecture.

---

# Current — Memory & Knowledge

## Memory, Storage & Retrieval

BindAI provides abstractions for memory, storage, embeddings, and retrieval.

### Completed

- [x] SQLite
- [x] PostgreSQL
- [x] Pinecone
- [x] Chroma
- [x] In-memory memory provider
- [x] Vector memory provider
- [x] Memory provider abstractions
- [x] BM25 retrieval
- [x] Vector retrieval
- [x] Hybrid retrieval
- [x] Embedding provider abstraction
- [x] Random/local embedding provider
- [x] OpenAI embeddings
- [x] Retrieval configuration
- [x] Search options

### Remaining

- [ ] Redis
- [ ] Qdrant
- [ ] pgvector
- [ ] Additional vector and storage providers
- [ ] Unified metadata filtering improvements across providers

The goal is to provide common BindAI interfaces while allowing applications to choose the storage technology that best fits their requirements.

---

## Advanced Knowledge & RAG

BindAI provides a knowledge and retrieval pipeline for knowledge-driven applications and agents.

### Completed

- [x] Document ingestion
- [x] Document loaders
- [x] Document parsing
- [x] Chunking strategies
- [x] Embeddings
- [x] Metadata
- [x] Semantic search
- [x] Hybrid search
- [x] Metadata filtering
- [x] Reranking
- [x] Lexical reranking
- [x] Conversational retrieval
- [x] Knowledge pipelines
- [x] Knowledge retrieval integration with agents
- [x] Retrieval configuration
- [x] Search options

### Remaining

- [ ] Citations
- [ ] Advanced document parsing
- [ ] Advanced chunking strategies
- [ ] Additional reranking strategies
- [ ] Advanced hybrid retrieval
- [ ] Advanced filtering
- [ ] Production-scale knowledge pipelines

---

# Current — Connections & Integrations

## Connections

BindAI provides a unified connections architecture for integrating applications with external services.

### Completed

#### Architecture

- [x] Connection abstraction
- [x] Connection registry
- [x] Connection manager
- [x] Connection lifecycle
- [x] Configurable base URLs
- [x] Authentication configuration
- [x] HTTP-based integration patterns
- [x] Integration testing
- [x] Project-scoped provider connections
- [x] Connection manifest metadata
- [x] Secure OS-backed provider credentials
- [x] CLI connection management
- [x] Connection-aware provider resolution
- [x] Connection validation in `bindai doctor`

#### Integrations

- [x] Webhook
- [x] GitHub
- [x] Slack
- [x] Notion
- [x] Jira
- [x] Discord
- [x] Resend
- [x] Vercel
- [x] Netlify
- [x] Google Sheets
- [x] Google Docs
- [x] Gmail
- [x] Google Drive

### Remaining

Additional integrations will be added based on developer and business use cases.

- [ ] Telegram
- [ ] Twilio
- [ ] Microsoft Outlook
- [ ] Microsoft Teams
- [ ] GitLab
- [ ] Linear
- [ ] Trello
- [ ] Asana
- [ ] Airtable
- [ ] HubSpot
- [ ] Salesforce
- [ ] Stripe
- [ ] Additional integrations

The goal is to make integrations modular and easy to create, configure, authenticate, and reuse.

---

# Current — MCP

## Model Context Protocol Integration

BindAI currently includes a lightweight HTTP-based MCP integration bridge.

This implementation should not be confused with a complete MCP protocol implementation. It provides a practical foundation for connecting BindAI tools to an external HTTP tool service while leaving full MCP protocol support for a later phase.

### Completed

- [x] MCP client package
- [x] Tool discovery through `GET /tools`
- [x] Tool calling through `POST /call`
- [x] MCP tools represented as BindAI tools
- [x] Tool metadata and parameter schema handling
- [x] BindAI execution context variables forwarded as tool arguments
- [x] HTTP error propagation
- [x] MCP integration tests
- [x] Basic HTTP connection bridge

### Remaining

- [ ] Full MCP protocol implementation
- [ ] MCP server implementation
- [ ] MCP resource discovery
- [ ] MCP prompts
- [ ] MCP authentication
- [ ] MCP sessions and lifecycle management
- [ ] MCP events and negotiation
- [ ] MCP resources as agent context
- [ ] Expanded MCP protocol support
- [ ] MCP SDK compatibility where appropriate

The current bridge is sufficient for the initial v0.1 integration scope. Full MCP support remains a post-v0.1 capability.

---

# Current — Agents & Multi-Agent Systems

## Advanced Agents & Multi-Agent Systems

The agent runtime already supports a substantial multi-agent foundation.

### Completed

- [x] Structured agent configuration
- [x] Context management
- [x] Agent memory
- [x] Delegation
- [x] Agent handoff
- [x] Specialist agents
- [x] Team delegation
- [x] Role-based agent chains
- [x] RAG-enabled agents
- [x] Agent groups
- [x] Parallel agents
- [x] Advanced tool execution

### Remaining

- [ ] Planning
- [ ] Supervisor agents
- [ ] Hierarchical multi-agent systems
- [ ] More advanced coordination strategies
- [ ] More robust multi-agent state management

The objective is to make complex AI systems composable from multiple specialized agents.

---

# Current — Automation

## AI Automation Platform

BindAI provides an automation layer that combines agents, workflows, integrations, triggers, state, history, and background execution.

### Completed

- [x] Webhooks
- [x] Scheduled execution
- [x] Conditional routing
- [x] Loops
- [x] Parallel execution
- [x] Retry policies
- [x] Timeouts
- [x] Human approval
- [x] Agent execution
- [x] External service integrations
- [x] Event trigger framework
- [x] Unified trigger management
- [x] Automation definitions
- [x] Persistent automation state abstraction
- [x] Automation run history
- [x] Background automation workers
- [x] In-process thread-pool execution
- [x] Automation run lifecycle tracking

### Remaining

- [ ] Advanced event routing
- [ ] Distributed automation workers
- [ ] Durable distributed execution
- [ ] Queue-backed automation execution
- [ ] Advanced scheduling and recovery

The current automation layer provides the foundation for defining, executing, tracking, and running automations in the background.

The v0.1 worker model is intentionally process-local. Distributed workers and queue-backed execution remain future infrastructure work.

---

# Current — Public API & Deployment

## REST API

BindAI now includes a public REST API package for exposing applications and runtime capabilities as services.

### Completed

- [x] Public API package
- [x] REST API
- [x] API authentication
- [x] API key authentication
- [x] Agent listing API
- [x] Agent execution API
- [x] Agent streaming API
- [x] Workflow listing API
- [x] Workflow execution API
- [x] Project API
- [x] Background automation run API
- [x] Run status API
- [x] Health endpoint
- [x] API tests
- [x] FastAPI integration

### Current limitations

- [x] Authentication is based on the configured `BINDAI_API_KEY`
- [x] API state is currently process-local
- [x] Background execution uses the in-process automation worker
- [x] Streaming currently uses HTTP `StreamingResponse`
- [ ] Distributed API state
- [ ] Distributed execution
- [ ] Queue-backed background jobs

---

## Deployment

### Completed

- [x] Docker deployment
- [x] Dockerfile
- [x] Docker Compose
- [x] API container execution
- [x] Environment-based configuration
- [x] Container health endpoint
- [x] Local container validation
- [x] Compose validation
- [x] Worker process foundation

### Remaining

- [ ] Production worker orchestration
- [ ] Queue-based execution
- [ ] Distributed workers
- [ ] Kubernetes deployment
- [ ] Horizontal execution scaling
- [ ] Durable distributed state

Queue-backed execution and Kubernetes are intentionally post-v0.1 infrastructure capabilities and should not block the initial public release.

---

# Current — Observability

## Runtime Observability

BindAI now has a structured event foundation for observing execution.

### Completed

- [x] Structured event model
- [x] Event IDs
- [x] Event timestamps
- [x] Event payloads
- [x] Event bus
- [x] Event subscriptions
- [x] Wildcard event subscriptions
- [x] Application lifecycle events
- [x] Agent execution events
- [x] Workflow execution events
- [x] Node execution events
- [x] Human task events
- [x] Model request events
- [x] Model response events
- [x] Tool execution events
- [x] Memory events
- [x] MCP event definitions
- [x] In-memory event recorder
- [x] Execution-level event lookup
- [x] Event recorder lifecycle management
- [x] Runtime observability integration

### Partially implemented

- [~] Execution history
- [~] Error visibility
- [~] Timing information
- [~] State transition visibility

The current observability layer provides structured runtime events and in-memory recording. It is intentionally lightweight and forms the foundation for future tracing, metrics, and external observability integrations.

### Remaining

- [ ] Distributed tracing
- [ ] Metrics
- [ ] Persistent execution history
- [ ] Token usage tracking
- [ ] Provider statistics
- [ ] Cost tracking
- [ ] Advanced latency analytics
- [ ] Advanced error tracking
- [ ] OpenTelemetry integration
- [ ] Monitoring integrations
- [ ] External observability backends
- [ ] Production dashboards

---

# Current — v0.1 Public Release

## Public Release Preparation

The initial public release is focused on making the core framework, API, deployment foundation, integrations, MCP bridge, automation, and observability capabilities usable by developers.

### Completed

- [x] Core framework foundation
- [x] Multi-agent foundation
- [x] Workflow engine
- [x] Automation foundation
- [x] Public REST API
- [x] API authentication
- [x] Streaming API
- [x] Background execution API
- [x] Docker deployment
- [x] Docker Compose
- [x] Core integrations
- [x] Google integrations
- [x] MCP HTTP bridge
- [x] Runtime event observability
- [x] Documentation pass
- [x] API documentation
- [x] Deployment documentation
- [x] Automated tests
- [x] Ruff validation
- [x] Ruff formatting
- [x] MyPy validation
- [x] Package builds
- [x] PyPI artifact validation
- [x] GitHub release-preparation checkpoint

### Release status

- [x] Package version reconciliation for the published release line
- [x] Dependency graph validation
- [x] Release workflow preparation
- [x] Final package builds
- [x] Final clean-install validation
- [x] PyPI publication of updated package versions
- [x] `bindai` 0.1.9 PyPI publication
- [x] Fresh public PyPI installation verification for `bindai==0.1.9`
- [x] Fresh public PyPI installation verification for `bindai-cli==0.2.2`
- [x] Published PyPI README synchronization
- [x] Documentation homepage Quick Start correction
- [ ] Final GitHub release/tag
- [ ] Final release announcement

The v0.1 release does not depend on Kubernetes, distributed queues, full MCP protocol support, advanced tracing, or enterprise infrastructure.

---

# Planned — Advanced Infrastructure

## Distributed Execution

After v0.1, BindAI can evolve from process-local execution toward distributed infrastructure.

### Planned

- [ ] Queue-based execution
- [ ] Durable job queues
- [ ] Distributed workers
- [ ] Worker pools
- [ ] Retry and recovery across workers
- [ ] Distributed state management
- [ ] Horizontal scaling
- [ ] Kubernetes deployment
- [ ] Durable scheduling
- [ ] Distributed automation execution

---

# Future — Enterprise Platform

## Enterprise Platform

As the platform matures, BindAI will introduce capabilities required by larger organizations.

### Planned

- [ ] Role-based access control
- [ ] Organizations and workspaces
- [ ] Multi-tenancy
- [ ] Permission management
- [ ] Audit logs
- [ ] Secret management
- [ ] Credential management
- [ ] Security controls
- [ ] Remote workers
- [ ] Distributed execution
- [ ] Worker pools
- [ ] Enterprise monitoring
- [ ] Governance capabilities
- [ ] Enterprise deployment controls

These features will provide the foundation for operating BindAI across larger teams and organizations.

---

# Future — Visual Workflow Platform

## Visual Workflow Platform

The long-term vision is to make BindAI workflows visually composable while preserving the underlying Python framework.

### Planned

- [ ] Drag-and-drop workflow design
- [ ] Agent nodes
- [ ] Tool nodes
- [ ] Condition nodes
- [ ] Loop nodes
- [ ] Parallel branches
- [ ] Human approval nodes
- [ ] Integration nodes
- [ ] Trigger nodes
- [ ] Scheduling
- [ ] Execution visualization
- [ ] Workflow debugging
- [ ] Agent visualization
- [ ] Workflow run history
- [ ] Visual execution inspection

Developers will be able to move between code-based and visual workflow development while using the same underlying execution engine.

---

# Future — Voice AI

## Voice AI

BindAI will eventually expand into voice-based AI applications.

### Planned

- [ ] Speech-to-text
- [ ] Text-to-speech
- [ ] Streaming audio
- [ ] Voice agents
- [ ] Conversational voice workflows
- [ ] Real-time interactions
- [ ] Phone integrations
- [ ] Voice memory and context

This will enable applications such as voice assistants, customer service systems, appointment assistants, and industry-specific voice agents.

---

# Future — Templates & Business Solutions

## Templates & Business Solutions

BindAI will provide complete templates demonstrating how the platform can be used to solve real-world problems.

### Planned examples

- [ ] AI Business Consultant
- [ ] Internal Knowledge Assistant
- [ ] Customer Support Agent
- [ ] HR Leave Automation
- [ ] Invoice Approval
- [ ] Document Processing
- [ ] Research Agent
- [ ] Sales Assistant
- [ ] Finance Assistant
- [ ] Dentist Voice Assistant
- [ ] Additional industry-specific solutions

These solutions will be developed as reusable examples, documentation tutorials, GitHub projects, and educational content.

---

# Long-Term Vision

BindAI is evolving toward a complete platform for building AI software.

The long-term architecture can be summarized as:

```text
                    BindAI
                       |
       +---------------+---------------+
       |               |               |
     Agents        Workflows        Knowledge
       |               |               |
       +---------------+---------------+
                       |
                  Integrations
                       |
              +--------+--------+
              |        |        |
             MCP    Providers  Tools
              |        |        |
              +--------+--------+
                       |
                 Automation
                       |
             +---------+---------+
             |         |         |
            API      Workers   Triggers
             |         |         |
             +---------+---------+
                       |
                Observability
                       |
                       v
                  Enterprise
                       |
                       v
              Visual Platform
                       |
                       v
                    Voice
```

The goal is not simply to provide another AI agent library.

The goal is to provide developers with the building blocks required to:

**Build → Automate → Deploy → Observe → Scale AI applications.**

---

# Build With Us

BindAI is open source and evolves through real-world usage, experimentation, and community feedback.

As new capabilities are introduced, the roadmap will continue to evolve while maintaining the same core principles:

- Python-first
- Modular
- Provider-agnostic
- Extensible
- Developer-friendly
- Production-oriented
- Open source

**Build AI Software. Scale Everywhere.**