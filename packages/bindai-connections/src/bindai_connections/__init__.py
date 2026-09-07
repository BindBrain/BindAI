"""BindAI connections and integrations."""

from .connection import Connection
from .manager import ConnectionManager
from .registry import ConnectionRegistry
from .webhook import WebhookConnection
from .github import GitHubConnection
from .slack import SlackConnection
from .notion import NotionConnection

ConnectionRegistry.register("webhook", WebhookConnection)
ConnectionRegistry.register("slack", SlackConnection)
ConnectionRegistry.register("notion", NotionConnection)

__version__ = "0.1.0"

__all__ = [
    "Connection",
    "ConnectionManager",
    "ConnectionRegistry",
    "WebhookConnection",
    "GitHubConnection",
    "SlackConnection",
    "NotionConnection",
]