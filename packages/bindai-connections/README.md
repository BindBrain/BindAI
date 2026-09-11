# BindAI Connections

`bindai-connections` provides integrations between BindAI applications and external services.

The package defines a common connection abstraction, connection management and registry components, together with built-in integrations for commonly used services.

## Features

* Connection abstraction
* Connection manager
* Connection registry
* Webhook integration
* Slack integration
* Notion integration
* Jira integration
* Discord integration
* Resend integration
* Vercel integration
* Netlify integration
* GitHub connection support
* Centralized connection registration

## Public API

The package exposes:

```python id="7m4q2x"
from bindai_connections import (
    Connection,
    ConnectionManager,
    ConnectionRegistry,
)
```

Built-in integrations include:

```python id="4r8n6v"
from bindai_connections import (
    WebhookConnection,
    SlackConnection,
    NotionConnection,
    JiraConnection,
    DiscordConnection,
    ResendConnection,
    VercelConnection,
    NetlifyConnection,
    GitHubConnection,
)
```

## Connection Abstraction

`Connection` provides the common abstraction for external service integrations.

```python id="8p3k1w"
from bindai_connections import Connection
```

This allows higher-level BindAI components to work with integrations through a consistent connection layer.

## Connection Manager

`ConnectionManager` provides the management layer for connections.

```python id="2x7m5q"
from bindai_connections import ConnectionManager

manager = ConnectionManager()
```

The manager can be used by applications that need to organize and work with multiple external integrations.

## Connection Registry

`ConnectionRegistry` provides centralized connection registration and lookup.

```python id="6n9v3r"
from bindai_connections import ConnectionRegistry
```

The package registers its built-in connection types under provider keys during initialization.

Current registered connection keys include:

```text id="5q8c2m"
webhook
slack
notion
jira
discord
resend
vercel
netlify
```

This allows integrations to be resolved through the registry instead of requiring consumers to hard-code a particular connection implementation.

## Supported Integrations

### Webhooks

`WebhookConnection` provides the connection abstraction for webhook-based integrations.

```python id="9v4k1x"
from bindai_connections import WebhookConnection
```

### Slack

`SlackConnection` provides the BindAI connection for Slack.

```python id="3m7p2n"
from bindai_connections import SlackConnection
```

### Notion

`NotionConnection` provides the BindAI connection for Notion.

```python id="1x6r8q"
from bindai_connections import NotionConnection
```

### Jira

`JiraConnection` provides the BindAI connection for Jira.

```python id="4n9w2k"
from bindai_connections import JiraConnection
```

### Discord

`DiscordConnection` provides the BindAI connection for Discord.

```python id="7c3m5v"
from bindai_connections import DiscordConnection
```

### Resend

`ResendConnection` provides the BindAI connection for Resend.

```python id="8k2q6p"
from bindai_connections import ResendConnection
```

### Vercel

`VercelConnection` provides the BindAI connection for Vercel.

```python id="5r7m1x"
from bindai_connections import VercelConnection
```

### Netlify

`NetlifyConnection` provides the BindAI connection for Netlify.

```python id="2p9v4n"
from bindai_connections import NetlifyConnection
```

### GitHub

`GitHubConnection` is also exposed as part of the public API.

```python id="6x3k8q"
from bindai_connections import GitHubConnection
```

## Architecture

The connections package separates external integrations from the rest of the BindAI application architecture:

```text id="9m5w2r"
BindAI Application / Agent
          │
          ▼
 ConnectionManager
          │
          ▼
 ConnectionRegistry
          │
    ┌─────┼────────────────────────┐
    │     │                        │
    ▼     ▼                        ▼
 Webhook Slack ...             GitHub
 Connection Connection          Connection
```

This keeps integration concerns isolated from application and agent execution logic.

## BindAI Integration

`bindai-connections` is intended for applications that need to communicate with external services.

Connections can be used as reusable integration components alongside BindAI applications, agents, workflows, and automation.

The package focuses on connection abstractions and integrations rather than implementing the core agent or workflow execution system.

## Version

The current package version exposed by the package is:

```python id="4q8n1v"
from bindai_connections import __version__

print(__version__)
```

Current version: `0.1.0`.

## Development

This package is part of the BindAI workspace.

From the repository root:

```bash id="7x2m6p"
uv sync
```

Run the complete test suite:

```bash id="3n9r5k"
uv run pytest
```

Run static type checking for this package:

```bash id="8v1c4q"
uv run mypy packages/bindai-connections
```

Build the package:

```bash id="6p3m8x"
uv build --package bindai-connections
```

## Documentation

For complete BindAI framework documentation:

https://docs.bindai.dev

## License

BindAI is released under the MIT License.
