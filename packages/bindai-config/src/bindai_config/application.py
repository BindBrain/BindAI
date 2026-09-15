from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ModelConfig:
    provider: str = "openai"

    model: str = "gpt-4.1-mini"

    temperature: float = 0.7

    max_tokens: int | None = None


@dataclass(slots=True)
class ApplicationAgentConfig:
    name: str

    instructions: str = ""

    model: ModelConfig | None = None


@dataclass(slots=True)
class ApplicationConfig:
    name: str

    description: str = ""

    type: str = "assistant"

    agent: ApplicationAgentConfig | None = None