from __future__ import annotations

from bindai_core.conversation import Conversation
from bindai_core.model import MessageRole


class ConversationQuery:
    """
    Builds a retrieval query from conversation history.
    """

    def __init__(
        self,
        max_messages: int = 6,
    ) -> None:
        self.max_messages = max_messages

    def build(
        self,
        conversation: Conversation,
    ) -> str:
        messages = [
            message
            for message in conversation.messages
            if message.role in {
                MessageRole.USER,
                MessageRole.ASSISTANT,
            }
            and message.content.strip()
        ]

        if not messages:
            return ""

        recent_messages = messages[-self.max_messages:]

        return "\n".join(
            f"{message.role.value}: {message.content.strip()}"
            for message in recent_messages
        )