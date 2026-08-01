from bindai_core import (
    Message,
    MessageRole,
    ModelRequest,
    ProviderConfiguration,
)
from bindai_provider_openai import OpenAIProvider

configuration = ProviderConfiguration(
    api_key="YOUR_API_KEY",
    model="gpt-5",
)

provider = OpenAIProvider(configuration)

request = ModelRequest(
    messages=[
        Message(
            role=MessageRole.USER,
            content="Say hello in one sentence.",
        )
    ]
)

response = provider.generate(request)

print(response.content)
print(response.usage)
