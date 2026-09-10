from __future__ import annotations

from bindai_core import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ProviderCapabilities,
    ProviderConfiguration,
    StreamChunk,
    TokenUsage,
)

from .client import GoogleClient
from .mapper import GoogleMapper


class GoogleProvider(ModelProvider):
    """
    Google Gemini implementation of ModelProvider.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):
        super().__init__(configuration)
        self._client = GoogleClient(configuration)

    @property
    def name(self) -> str:
        return "google"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            chat=True,
            streaming=True,
            vision=True,
            embeddings=False,
            tool_calling=True,
            structured_output=True,
            reasoning=True,
        )

    def _build_kwargs(
        self,
        request: ModelRequest,
    ) -> dict:
        system, messages = GoogleMapper.messages(
            request.messages,
        )

        kwargs: dict[str, object] = {
            "model": self.configuration.model,
            "contents": messages,
        }

        config: dict[str, object] = {}

        if system is not None:
            config["system_instruction"] = system

        if request.temperature is not None:
            config["temperature"] = request.temperature

        if request.max_tokens is not None:
            config["max_output_tokens"] = request.max_tokens

        if request.top_p is not None:
            config["top_p"] = request.top_p

        if request.stop is not None:
            config["stop_sequences"] = request.stop

        if config:
            kwargs["config"] = config

        return kwargs

    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        response = self._client.client.models.generate_content(
            **self._build_kwargs(request),
        )

        usage_metadata = response.usage_metadata

        usage = TokenUsage(
            prompt_tokens=(usage_metadata.prompt_token_count or 0) if usage_metadata else 0,
            completion_tokens=(usage_metadata.candidates_token_count or 0) if usage_metadata else 0,
            total_tokens=(usage_metadata.total_token_count or 0) if usage_metadata else 0,
        )

        content = response.text or ""

        finish_reason = None

        if response.candidates:
            finish_reason = str(response.candidates[0].finish_reason)

        return ModelResponse(
            content=content,
            usage=usage,
            finish_reason=finish_reason,
            model=response.model_version or self.configuration.model,
        )

    def stream(
        self,
        request: ModelRequest,
    ):
        response = self._client.client.models.generate_content_stream(
            **self._build_kwargs(request),
        )

        for chunk in response:
            text = chunk.text or ""

            if text:
                yield StreamChunk(
                    delta=text,
                )

        yield StreamChunk(
            delta="",
            finished=True,
        )
