from bindai_agent import AgentBuilder
from bindai_core import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ProviderCapabilities,
)
from bindai_providers import ProviderRegistry


class EchoProvider(ModelProvider):
    def __init__(self, configuration=None):
        self.configuration = configuration

    @property
    def name(self):
        return "echo"

    @property
    def capabilities(self):
        return ProviderCapabilities()

    def generate(self, request: ModelRequest) -> ModelResponse:
        prompt = request.messages[-1].content

        return ModelResponse(
            content=f"Echo provider received: {prompt}",
        )

    def stream(self, request: ModelRequest):
        yield from ()


ProviderRegistry.register(
    "echo",
    lambda **kwargs: EchoProvider(),
)


agent = (
    AgentBuilder()
    .provider("echo")
    .build()
)

result = agent.chat(
    "Hello custom provider!",
)

print(result)