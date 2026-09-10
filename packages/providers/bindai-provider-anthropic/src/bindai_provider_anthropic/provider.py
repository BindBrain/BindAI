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

from .client import AnthropicClient
from .mapper import AnthropicMapper


class AnthropicProvider(ModelProvider):
    """
    Anthropic implementation of ModelProvider.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):
        super().__init__(configuration)
        self._client = AnthropicClient(configuration)

    @property
    def name(self) -> str:
        return "anthropic"

    def _build_kwargs(
        self,
        request: ModelRequest,
    ) -> dict:
        system, messages = AnthropicMapper.messages(
            request.messages,
        )

        kwargs: dict[str, object] = {
            "model": self.configuration.model,
            "max_tokens": request.max_tokens or 1024,
            "messages": messages,
        }

        if system is not None:
            kwargs["system"] = system

        if request.tools:
            kwargs["tools"] = AnthropicMapper.tools(
                request.tools,
            )

        if request.temperature is not None:
            kwargs["temperature"] = request.temperature

        if request.top_p is not None:
            kwargs["top_p"] = request.top_p

        if request.stop is not None:
            kwargs["stop_sequences"] = request.stop

        return kwargs

    def generate(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        response = self._client.client.messages.create(
            **self._build_kwargs(request),
        )

        usage = TokenUsage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=(response.usage.input_tokens + response.usage.output_tokens),
        )

        content = ""
        if response.content:
            text_parts = [
                block.text for block in response.content if getattr(block, "type", None) == "text"
            ]
            content = "".join(text_parts)

        structured_output = None

        if request.response_schema is not None and content:
            data = json.loads(content)
            structured_output = request.response_schema.model(
                **data,
            )

        return ModelResponse(
            content=content,
            usage=usage,
            tool_calls=AnthropicMapper.tool_calls(
                response.content,
            ),
            finish_reason=response.stop_reason,
            model=response.model,
            structured_output=structured_output,
        )

    def stream(
        self,
        request: ModelRequest,
    ):
        response = self._client.client.messages.create(
            stream=True,
            **self._build_kwargs(request),
        )

        for event in response:
            if getattr(event, "type", None) != "content_block_delta":
                continue

            delta = getattr(event, "delta", None)

            if getattr(delta, "type", None) != "text_delta":
                continue

            text = getattr(delta, "text", None)

            if text:
                yield StreamChunk(
                    delta=text,
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
            vision=True,
            embeddings=False,
            tool_calling=True,
            structured_output=True,
            reasoning=True,
        )
