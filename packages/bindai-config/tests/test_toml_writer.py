from pathlib import Path

import pytest
from bindai_config import TomlWriter


def test_toml_writer_updates_existing_value(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
name = "demo"
provider = "openai"
model = "gpt-4.1-mini"
temperature = 0.7
timeout = 60
""".strip()
        + "\n",
        encoding="utf-8",
    )

    TomlWriter().set(
        config_path,
        "provider",
        "anthropic",
    )

    assert config_path.read_text(encoding="utf-8") == (
        """
name = "demo"
provider = "anthropic"
model = "gpt-4.1-mini"
temperature = 0.7
timeout = 60
""".strip()
        + "\n"
    )


def test_toml_writer_adds_missing_known_field(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        'name = "demo"\n',
        encoding="utf-8",
    )

    TomlWriter().set(
        config_path,
        "provider",
        "anthropic",
    )

    assert config_path.read_text(encoding="utf-8") == (
        'name = "demo"\nprovider = "anthropic"\n'
    )


def test_toml_writer_preserves_comments_and_unrelated_content(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
# Project configuration
name = "demo"

# Model configuration
provider = "openai" # Current provider
model = "gpt-4.1-mini"

# Runtime
timeout = 60
""".strip()
        + "\n",
        encoding="utf-8",
    )

    TomlWriter().set(
        config_path,
        "provider",
        "anthropic",
    )

    content = config_path.read_text(encoding="utf-8")

    assert "# Project configuration" in content
    assert "# Model configuration" in content
    assert 'provider = "anthropic" # Current provider' in content
    assert 'model = "gpt-4.1-mini"' in content
    assert "# Runtime" in content
    assert "timeout = 60" in content


def test_toml_writer_writes_typed_values(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
temperature = 0.7
timeout = 60
""".strip()
        + "\n",
        encoding="utf-8",
    )

    writer = TomlWriter()
    writer.set(config_path, "temperature", 0.3)
    writer.set(config_path, "timeout", 120)

    content = config_path.read_text(encoding="utf-8")

    assert "temperature = 0.3" in content
    assert "timeout = 120" in content


def test_toml_writer_rejects_unknown_field(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        'name = "demo"\n',
        encoding="utf-8",
    )

    with pytest.raises(
        KeyError,
        match='Unknown configuration field "unknown"',
    ):
        TomlWriter().set(
            config_path,
            "unknown",
            "value",
        )


def test_toml_writer_rejects_invalid_value_type(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        "timeout = 60\n",
        encoding="utf-8",
    )

    with pytest.raises(
        TypeError,
        match='Invalid value for configuration field "timeout"',
    ):
        TomlWriter().set(
            config_path,
            "timeout",
            "not-an-int",
        )


def test_toml_writer_does_not_modify_file_on_validation_failure(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "bindai.toml"
    original = 'name = "demo"\ntimeout = 60\n'
    config_path.write_text(
        original,
        encoding="utf-8",
    )

    with pytest.raises(TypeError):
        TomlWriter().set(
            config_path,
            "timeout",
            "invalid",
        )

    assert config_path.read_text(encoding="utf-8") == original


def test_toml_writer_rejects_nested_configuration(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[agent]
name = "Assistant"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="top-level configuration fields",
    ):
        TomlWriter().set(
            config_path,
            "provider",
            "openai",
        )