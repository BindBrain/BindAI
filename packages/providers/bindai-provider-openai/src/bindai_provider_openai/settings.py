from dataclasses import dataclass


@dataclass(slots=True)
class OpenAISettings:

    api_key: str

    model: str = "gpt-5"

    base_url: str | None = None