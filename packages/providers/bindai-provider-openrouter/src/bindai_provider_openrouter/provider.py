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

from .client import OpenRouterClient
from .mapper import OpenRouterMapper


class OpenRouterProvider(ModelProvider):
    def __init__(self, configuration: ProviderConfiguration):
        super().__init__(configuration)
        self._client = OpenRouterClient(configuration)

    @property
    def name(self) -> str:
        return "openrouter"

    def _build_kwargs(self, request: ModelRequest) -> dict:
        kwargs: dict[str, object] = {
            "model": self.configuration.model,
            "messages": OpenRouterMapper.messages(request.messages),
        }

        if request.tools:
            kwargs["tools"] = OpenRouterMapper.tools(request.tools)

        if request.response_schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": request.response_schema.model.__name__,
                    "schema": request.response_schema.json_schema,
                },
            }

        if request.temperature is not None:
            kwargs["temperature"] = request.temperature

        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens

        if request.top_p is not None:
            kwargs["top_p"] = request.top_p

        if request.frequency_penalty is not None:
            kwargs["frequency_penalty"] = request.frequency_penalty

        if request.presence_penalty is not None:
            kwargs["presence_penalty"] = request.presence_penalty

        if request.stop is not None:
            kwargs["stop"] = request.stop

        return kwargs

    def generate(self, request: ModelRequest) -> ModelResponse:
        response = self._client.client.chat.completions.create(
            **self._build_kwargs(request),
        )

        choice = response.choices[0]
        message = choice.message

        usage_data = response.usage

        prompt_tokens = usage_data.prompt_tokens if usage_data else 0
        completion_tokens = usage_data.completion_tokens if usage_data else 0

        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )

        content = message.content or ""
        structured_output = None

        if request.response_schema is not None and content:
            data = json.loads(content)
            structured_output = request.response_schema.model(**data)

        return ModelResponse(
            content=content,
            tool_calls=OpenRouterMapper.tool_calls(message),
            usage=usage,
            finish_reason=choice.finish_reason,
            model=response.model,
            structured_output=structured_output,
        )

    def stream(self, request: ModelRequest):
        response = self._client.client.chat.completions.create(
            **self._build_kwargs(request),
            stream=True,
        )

        for chunk in response:
            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content or ""

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