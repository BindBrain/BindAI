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

    def _build_kwargs(
        self,
        request: ModelRequest,
    ) -> dict:

        kwargs: dict[str, object] = {
            "model": self.configuration.model,
            "messages": OpenAIMapper.messages(
                request.messages,
            ),
        }

        if request.response_schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": (request.response_schema.model.__name__),
                    "schema": (request.response_schema.json_schema),
                },
            }

        if request.tools:
            kwargs["tools"] = OpenAIMapper.tools(
                request.tools,
            )

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

    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:

        response = self._client.client.chat.completions.create(
            **self._build_kwargs(
                request,
            ),
        )

        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

        structured_output = None

        if request.response_schema is not None:
            data = json.loads(response.choices[0].message.content)

            structured_output = request.response_schema.model(
                **data,
            )

        return ModelResponse(
            content=response.choices[0].message.content or "",
            usage=usage,
            tool_calls=OpenAIMapper.tool_calls(
                response.choices[0].message,
            ),
            structured_output=structured_output,
        )

    def stream(
        self,
        request: ModelRequest,
    ):

        response = self._client.client.chat.completions.create(
            stream=True,
            **self._build_kwargs(
                request,
            ),
        )

        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                yield StreamChunk(
                    delta=delta,
                )

        yield StreamChunk(
            delta="",
            finished=True,
        )

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities()
