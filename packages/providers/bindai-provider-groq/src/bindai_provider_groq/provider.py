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

from .client import GroqClient
from .mapper import GroqMapper


class GroqProvider(ModelProvider):
    """
    Groq implementation of ModelProvider.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):
        super().__init__(configuration)

        self._client = GroqClient(configuration)

    @property
    def name(self) -> str:
        return "groq"

    def _build_kwargs(
        self,
        request: ModelRequest,
    ) -> dict:
        kwargs: dict[str, object] = {
            "model": self.configuration.model,
            "messages": GroqMapper.messages(
                request.messages,
            ),
        }

        if request.response_schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": request.response_schema.model.__name__,
                    "schema": request.response_schema.json_schema,
                },
            }

        if request.tools:
            kwargs["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in request.tools
            ]

        if request.temperature is not None:
            kwargs["temperature"] = request.temperature

        if request.max_tokens is not None:
            kwargs["max_completion_tokens"] = request.max_tokens

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
            **self._build_kwargs(request),
        )

        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

        structured_output = None

        if request.response_schema is not None:
            data = json.loads(
                response.choices[0].message.content,
            )

            structured_output = request.response_schema.model(
                **data,
            )

        return ModelResponse(
            content=response.choices[0].message.content or "",
            usage=usage,
            tool_calls=GroqMapper.tool_calls(
                response.choices[0].message,
            ),
            structured_output=structured_output,
            finish_reason=response.choices[0].finish_reason,
            model=response.model,
        )

    def stream(
        self,
        request: ModelRequest,
    ):
        response = self._client.client.chat.completions.create(
            stream=True,
            **self._build_kwargs(request),
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
        return ProviderCapabilities(
            chat=True,
            streaming=True,
            vision=False,
            embeddings=False,
            tool_calling=True,
            structured_output=True,
            reasoning=True,
        )
