from __future__ import annotations

import os
from pathlib import Path

from bindai_config import ProjectRuntime
from bindai_providers import (
    ProviderConfiguration,
    ProviderRegistry,
    bootstrap,
)
from dotenv import load_dotenv

_PROVIDER_ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "ollama": "OLLAMA_HOST",
    "openrouter": "OPENROUTER_API_KEY",
}


def resolve_provider(
    provider: str | object,
    *,
    api_key: str | None = None,
    endpoint: str | None = None,
    organization: str | None = None,
    model: str | None = None,
    timeout: int | None = None,
):
    if not isinstance(provider, str):
        return provider

    load_dotenv()
    bootstrap()

    provider_name = provider.lower()

    project = ProjectRuntime(Path.cwd()).config

    env_api_key = None
    env_endpoint = None
    env_organization = None

    env_key = _PROVIDER_ENV_KEYS.get(provider_name)

    if env_key:
        value = os.getenv(env_key)

        if provider_name == "ollama":
            env_endpoint = value
        else:
            env_api_key = value

    if provider_name == "openai":
        env_endpoint = os.getenv("OPENAI_BASE_URL")
        env_organization = os.getenv("OPENAI_ORGANIZATION")

    configuration = ProviderConfiguration(
        api_key=api_key if api_key is not None else env_api_key,
        endpoint=endpoint if endpoint is not None else env_endpoint,
        organization=(
            organization
            if organization is not None
            else env_organization
        ),
        model=model if model is not None else project.model,
        timeout=timeout if timeout is not None else project.timeout,
    )

    return ProviderRegistry.create(
        provider_name,
        configuration=configuration,
    )
