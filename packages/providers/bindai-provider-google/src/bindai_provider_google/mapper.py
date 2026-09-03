from __future__ import annotations

from bindai_core import Message, MessageRole


class GoogleMapper:
    """
    Converts BindAI messages into Google Gemini SDK-compatible content.
    """

    @staticmethod
    def messages(
        messages: list[Message],
    ) -> tuple[str | None, list[dict]]:
        system: str | None = None
        result: list[dict] = []

        for message in messages:
            if message.role == MessageRole.SYSTEM:
                system = message.content
                continue

            if message.role == MessageRole.USER:
                result.append(
                    {
                        "role": "user",
                        "parts": [{"text": message.content}],
                    }
                )
                continue

            if message.role == MessageRole.ASSISTANT:
                result.append(
                    {
                        "role": "model",
                        "parts": [{"text": message.content}],
                    }
                )
                continue

            if message.role == MessageRole.TOOL:
                result.append(
                    {
                        "role": "user",
                        "parts": [{"text": message.content}],
                    }
                )

        return system, result
