from pathlib import Path

import pytest
from bindai_connections.manifest import (
    ConnectionManifest,
    ConnectionMetadata,
)


def test_missing_manifest_is_empty(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    assert manifest.list() == []


def test_add_and_get_connection(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    manifest.add(" OpenAI ", " OpenAI ")

    assert manifest.get("OPENAI") == ConnectionMetadata(
        name="openai",
        provider="openai",
    )


def test_add_persists_non_secret_metadata(tmp_path: Path):
    path = tmp_path / "connections.toml"
    manifest = ConnectionManifest(path)

    manifest.add("openai", "openai")

    content = path.read_text(encoding="utf-8")

    assert 'name = "openai"' in content
    assert 'provider = "openai"' in content


def test_add_replaces_existing_connection(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    manifest.add("openai", "openai")
    manifest.add("openai", "openrouter")

    assert manifest.list() == [
        ConnectionMetadata(
            name="openai",
            provider="openrouter",
        ),
    ]


def test_remove_connection(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    manifest.add("openai", "openai")
    manifest.remove("openai")

    assert manifest.list() == []


def test_remove_missing_connection_is_safe(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    manifest.remove("openai")

    assert manifest.list() == []


def test_empty_name_is_rejected(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    with pytest.raises(ValueError, match="Connection name cannot be empty"):
        manifest.add("", "openai")


def test_empty_provider_is_rejected(tmp_path: Path):
    manifest = ConnectionManifest(tmp_path / "connections.toml")

    with pytest.raises(ValueError, match="Provider cannot be empty"):
        manifest.add("openai", "")


def test_invalid_manifest_shape_is_rejected(tmp_path: Path):
    path = tmp_path / "connections.toml"
    path.write_text(
        "[connections]\nname = 'openai'\n",
        encoding="utf-8",
    )

    manifest = ConnectionManifest(path)

    with pytest.raises(ValueError, match="must contain an array"):
        manifest.list()