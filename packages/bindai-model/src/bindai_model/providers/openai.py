from __future__ import annotations

from openai import OpenAI

from bindai_model.provider import ModelProvider
from bindai_model.result import ModelResult


class OpenAIProvider(ModelProvider):
    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        api_key: str | None = None,
    ):
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> ModelResult:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            **kwargs,
        )

        message = response.choices[0].message.content or ""

        return ModelResult(
            content=message,
            model=self.model,
            provider="openai",
            finish_reason=response.choices[0].finish_reason,
            usage=response.usage.model_dump() if response.usage else None,
        )
