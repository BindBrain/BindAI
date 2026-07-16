from bindai_core.model import (
    Message,
    MessageRole,
    ModelRequest,
)

from bindai_provider_openai import (
    OpenAIProvider,
    OpenAISettings,
)

settings = OpenAISettings(
    api_key="YOUR_API_KEY",
)

provider = OpenAIProvider(settings)

response = provider.generate(

    ModelRequest(

        messages=[
            Message(
                role=MessageRole.USER,
                content="What is BindAI?"
            )
        ]

    )

)

print(response.content)