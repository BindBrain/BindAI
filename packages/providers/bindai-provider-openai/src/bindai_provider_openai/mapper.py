from bindai_core.model import ModelRequest


class OpenAIMapper:

    @staticmethod
    def messages(request: ModelRequest):

        return [

            {
                "role": message.role.value,
                "content": message.content,
            }

            for message in request.messages

        ]