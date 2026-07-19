from __future__ import annotations

from bindai_core.model import (
    Message,
    MessageRole,
)

from .memory import Memory


class ChatMemory(Memory):
    """
    Conversation memory for an agent.
    """

    def add(
        self,
        message: Message,
    ) -> None:

        messages = self.load()

        messages.append(
            message,
        )

        self.save(
            messages,
        )

    def add_user(
        self,
        text: str,
    ) -> None:

        self.add(

            Message(

                role=MessageRole.USER,

                content=text,

            )

        )

    def add_assistant(
        self,
        text: str,
    ) -> None:

        self.add(

            Message(

                role=MessageRole.ASSISTANT,

                content=text,

            )

        )

    def add_system(
        self,
        text: str,
    ) -> None:

        self.add(

            Message(

                role=MessageRole.SYSTEM,

                content=text,

            )

        )

    def messages(
        self,
    ) -> list[Message]:
        """
        Return a copy of all stored messages.
        """

        return self.load()