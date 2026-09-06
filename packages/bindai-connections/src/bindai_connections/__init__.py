"""BindAI connections and integrations."""

from .connection import Connection
from .registry import ConnectionRegistry
from .webhook import WebhookConnection

ConnectionRegistry.register("webhook", WebhookConnection)

__version__ = "0.1.0"

__all__ = [
    "Connection",
    "ConnectionRegistry",
    "WebhookConnection",
]