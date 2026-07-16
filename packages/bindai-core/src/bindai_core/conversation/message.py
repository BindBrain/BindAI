from dataclasses import dataclass

from bindai_core.model import MessageRole


@dataclass(slots=True)
class ConversationMessage:

    role: MessageRole

    content: str