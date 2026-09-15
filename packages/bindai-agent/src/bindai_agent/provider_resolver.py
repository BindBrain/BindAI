from __future__ import annotations

import os
from pathlib import Path

from bindai_config import (
    ProjectRuntime,
    get_provider_connection,
)
from bindai_connections import (
    ConnectionManifest,
    KeyringProviderCredentialStore,
)
from bindai_providers import (
    ProviderConfiguration,
    ProviderRegistry,
    bootstrap,
)
from dotenv import load_dotenv


def resolve_provider(
    provider: str | object,
    *,
    api_key: str | None = None,
    endpoint: str | None = None,
    organization: str | None = None,
    model: str | None = None,
    timeout: int | None = None,
    connection: str | None = None,
):
    if not isinstance(provider, str):
        return provider

    load_dotenv()
    bootstrap()

    provider_name = provider.lower()
    provider_connection = get_provider_connection(provider_name)

    project = ProjectRuntime(Path.cwd()).config

    env_api_key = None
    env_endpoint = None
    env_organization = None

    if provider_connection.api_key_env:
        env_api_key = os.getenv(
            provider_connection.api_key_env,
        )

    if provider_connection.endpoint_env:
        env_endpoint = os.getenv(
            provider_connection.endpoint_env,
        )

    if provider_connection.organization_env:
        env_organization = os.getenv(
            provider_connection.organization_env,
        )

    connection_api_key = None

    if connection is not None:
        manifest = ConnectionManifest(
            Path.cwd() / ".bindai" / "connections.toml",
        )

        metadata = manifest.get(connection)

        if metadata is None:
            raise ValueError(
                f'Connection "{connection}" is not configured.',
            )

        if metadata.provider != provider_name:
            raise ValueError(
                f'Connection "{connection}" uses provider '
                f'"{metadata.provider}", not "{provider_name}".',
            )

        store = KeyringProviderCredentialStore()

        connection_api_key = store.get(
            metadata.name,
        )

    configuration = ProviderConfiguration(
        api_key=(
            api_key
            if api_key is not None
            else (
                connection_api_key
                if connection_api_key is not None
                else env_api_key
            )
        ),
        endpoint=(
            endpoint
            if endpoint is not None
            else env_endpoint
        ),
        organization=(
            organization
            if organization is not None
            else env_organization
        ),
        model=(
            model
            if model is not None
            else project.model
        ),
        timeout=(
            timeout
            if timeout is not None
            else project.timeout
        ),
    )

    return ProviderRegistry.create(
        provider_name,
        configuration=configuration,
    )