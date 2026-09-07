"""BindAI connections and integrations."""

from .connection import Connection
from .manager import ConnectionManager
from .registry import ConnectionRegistry
from .webhook import WebhookConnection
from .github import GitHubConnection

ConnectionRegistry.register("webhook", WebhookConnection)

__version__ = "0.1.0"

__all__ = [
    "Connection",
    "ConnectionManager",
    "ConnectionRegistry",
    "WebhookConnection",
    "GitHubConnection",
]