from __future__ import annotations

from bindai_core import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ProviderCapabilities,
    ProviderConfiguration,
    TokenUsage,
)

from .client import OpenAIClient
from .mapper import OpenAIMapper


class OpenAIProvider(ModelProvider):
    """
    OpenAI implementation of ModelProvider.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):
        super().__init__(configuration)

        self._client = OpenAIClient(configuration)

    @property
    def name(self) -> str:
        return "openai"

    @property
    def capabilities(self) -> ProviderCapabilities:

        capabilities = ProviderCapabilities()

        capabilities.streaming = True
        capabilities.tool_calling = True

        return capabilities

    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:

        response = self._client.client.chat.completions.create(

            model=self.configuration.model,

            messages=OpenAIMapper.messages(
                request.messages,
            ),

            temperature=request.temperature,

            max_tokens=request.max_tokens,

            top_p=request.top_p,

            frequency_penalty=request.frequency_penalty,

            presence_penalty=request.presence_penalty,

            stop=request.stop,
        )

        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

        return ModelResponse(
            content=response.choices[0].message.content or "",
            usage=usage,
        )