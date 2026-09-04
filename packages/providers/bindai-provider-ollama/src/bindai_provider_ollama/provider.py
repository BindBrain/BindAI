from __future__ import annotations

import json

from bindai_core import (
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ProviderCapabilities,
    ProviderConfiguration,
    StreamChunk,
    TokenUsage,
)

from .client import OllamaClient
from .mapper import OllamaMapper


class OllamaProvider(ModelProvider):
    def __init__(self, configuration: ProviderConfiguration):
        super().__init__(configuration)
        self._client = OllamaClient(configuration)

    @property
    def name(self) -> str:
        return "ollama"

    def _build_kwargs(self, request: ModelRequest) -> dict:
        kwargs: dict[str, object] = {
            "model": self.configuration.model,
            "messages": OllamaMapper.messages(request.messages),
        }

        if request.response_schema is not None:
            kwargs["format"] = request.response_schema.json_schema

        options: dict[str, object] = {}

        if request.temperature is not None:
            options["temperature"] = request.temperature

        if request.max_tokens is not None:
            options["num_predict"] = request.max_tokens

        if request.top_p is not None:
            options["top_p"] = request.top_p

        if request.stop is not None:
            options["stop"] = request.stop

        if options:
            kwargs["options"] = options

        return kwargs

    def generate(self, request: ModelRequest) -> ModelResponse:
        response = self._client.client.chat(
            **self._build_kwargs(request),
        )

        prompt_tokens = response.prompt_eval_count or 0
        completion_tokens = response.eval_count or 0

        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )

        structured_output = None

        if request.response_schema is not None:
            content = response.message.content or ""
            data = json.loads(content)
            structured_output = request.response_schema.model(**data)

        return ModelResponse(
            content=response.message.content or "",
            usage=usage,
            tool_calls=OllamaMapper.tool_calls(response.message),
            structured_output=structured_output,
            finish_reason=response.done_reason,
            model=response.model,
        )

    def stream(self, request: ModelRequest):
        response = self._client.client.chat(
            **self._build_kwargs(request),
            stream=True,
        )

        for chunk in response:
            content = chunk.message.content or ""

            if content:
                yield StreamChunk(delta=content)

        yield StreamChunk(delta="", finished=True)

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