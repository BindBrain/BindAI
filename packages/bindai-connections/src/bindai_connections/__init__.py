"""BindAI connections and integrations."""

from .connection import Connection
from .discord import DiscordConnection
from .github import GitHubConnection
from .gmail import GmailConnection
from .google_docs import GoogleDocsConnection
from .google_drive import GoogleDriveConnection
from .google_sheets import GoogleSheetsConnection
from .jira import JiraConnection
from .manager import ConnectionManager
from .netlify import NetlifyConnection
from .notion import NotionConnection
from .registry import ConnectionRegistry
from .resend import ResendConnection
from .slack import SlackConnection
from .vercel import VercelConnection
from .webhook import WebhookConnection

ConnectionRegistry.register("webhook", WebhookConnection)
ConnectionRegistry.register("slack", SlackConnection)
ConnectionRegistry.register("notion", NotionConnection)
ConnectionRegistry.register("jira", JiraConnection)
ConnectionRegistry.register("discord", DiscordConnection)
ConnectionRegistry.register("resend", ResendConnection)
ConnectionRegistry.register("vercel", VercelConnection)
ConnectionRegistry.register("netlify", NetlifyConnection)
ConnectionRegistry.register("google_sheets", GoogleSheetsConnection)
ConnectionRegistry.register("google_docs", GoogleDocsConnection)
ConnectionRegistry.register("gmail", GmailConnection)
ConnectionRegistry.register("google_drive", GoogleDriveConnection)

__version__ = "0.1.0"

__all__ = [
    "Connection",
    "ConnectionManager",
    "ConnectionRegistry",
    "WebhookConnection",
    "GitHubConnection",
    "SlackConnection",
    "NotionConnection",
    "JiraConnection",
    "DiscordConnection",
    "ResendConnection",
    "VercelConnection",
    "NetlifyConnection",
    "GoogleSheetsConnection",
    "GoogleDocsConnection",
    "GmailConnection",
    "GoogleDriveConnection",
]
