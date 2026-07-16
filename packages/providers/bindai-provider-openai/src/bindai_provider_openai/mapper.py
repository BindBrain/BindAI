from bindai_core import Message


class OpenAIMapper:
    """
    Converts BindAI models into OpenAI SDK models.
    """

    @staticmethod
    def messages(
        messages: list[Message],
    ) -> list[dict]:

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]