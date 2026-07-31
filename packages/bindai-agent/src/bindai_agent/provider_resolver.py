from __future__ import annotations

import os
from pathlib import Path

from bindai_config import ProjectRuntime
from bindai_providers import (
    ProviderConfiguration,
    ProviderRegistry,
)


def resolve_provider(provider):
    """
    Resolves either:

    - an already constructed provider
    - or a provider name ("openai")
    """

    if not isinstance(provider, str):
        return provider

    project = ProjectRuntime(
        Path.cwd(),
    ).config

    configuration = ProviderConfiguration(
        api_key=os.getenv("OPENAI_API_KEY"),
        endpoint=os.getenv("OPENAI_BASE_URL"),
        organization=os.getenv("OPENAI_ORGANIZATION"),
        model=project.model,
        timeout=project.timeout,
    )

    return ProviderRegistry.create(
        provider,
        configuration=configuration,
    )