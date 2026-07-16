from dataclasses import dataclass


@dataclass(slots=True)
class OpenAISettings:
    """
    Configuration for the OpenAI provider.
    """

    api_key: str

    model: str = "gpt-5"

    base_url: str | None = None

    organization: str | None = None

    timeout: float = 60.0