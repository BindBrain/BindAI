from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from bindai_core.model import MessageRole


@dataclass(slots=True)
class ConversationMessage:
    """
    One message stored in a conversation.
    """

    role: MessageRole

    content: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )