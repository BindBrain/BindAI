from pathlib import Path

from bindai_cli.app import app
from typer.testing import CliRunner

runner = CliRunner()


def test_connections_help_lists_add_list_and_remove():
    result = runner.invoke(
        app,
        ["connections", "--help"],
    )

    assert result.exit_code == 0
    assert "add" in result.stdout
    assert "list" in result.stdout
    assert "remove" in result.stdout


def test_connections_add_stores_credential_and_manifest(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    stored: dict[tuple[str, str], str] = {}

    class FakeKeyring:
        def set_password(
            self,
            service: str,
            username: str,
            password: str,
        ) -> None:
            stored[(service, username)] = password

        def get_password(
            self,
            service: str,
            username: str,
        ) -> str | None:
            return stored.get((service, username))

        def delete_password(
            self,
            service: str,
            username: str,
        ) -> None:
            stored.pop((service, username), None)

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        ["connections", "add", "openai"],
        input="secret-key\n",
    )

    assert result.exit_code == 0
    assert 'Connection "openai" added for provider "openai".' in result.stdout

    assert stored[("bindai", "openai")] == "secret-key"

    manifest = (
        tmp_path
        / ".bindai"
        / "connections.toml"
    )

    assert manifest.exists()

    content = manifest.read_text(encoding="utf-8")

    assert 'name = "openai"' in content
    assert 'provider = "openai"' in content
    assert "secret-key" not in content


def test_connections_add_supports_custom_name(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    stored: dict[tuple[str, str], str] = {}

    class FakeKeyring:
        def set_password(self, service, username, password):
            stored[(service, username)] = password

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        [
            "connections",
            "add",
            "openai",
            "--name",
            "work",
        ],
        input="secret-key\n",
    )

    assert result.exit_code == 0
    assert stored[("bindai", "work")] == "secret-key"

    manifest = (
        tmp_path
        / ".bindai"
        / "connections.toml"
    )

    content = manifest.read_text(encoding="utf-8")

    assert 'name = "work"' in content
    assert 'provider = "openai"' in content


def test_connections_add_keeps_credentials_for_two_named_connections(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    stored: dict[tuple[str, str], str] = {}

    class FakeKeyring:
        def set_password(self, service, username, password):
            stored[(service, username)] = password

        def get_password(self, service, username):
            return stored.get((service, username))

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    work_result = runner.invoke(
        app,
        [
            "connections",
            "add",
            "openai",
            "--name",
            "work",
        ],
        input="sk-WORK-KEY\n",
    )

    personal_result = runner.invoke(
        app,
        [
            "connections",
            "add",
            "openai",
            "--name",
            "personal",
        ],
        input="sk-PERSONAL-KEY\n",
    )

    assert work_result.exit_code == 0
    assert personal_result.exit_code == 0

    assert stored[("bindai", "work")] == "sk-WORK-KEY"
    assert stored[("bindai", "personal")] == "sk-PERSONAL-KEY"

    manifest = (
        tmp_path
        / ".bindai"
        / "connections.toml"
    )

    content = manifest.read_text(encoding="utf-8")

    assert 'name = "work"' in content
    assert 'name = "personal"' in content
    assert "sk-WORK-KEY" not in content
    assert "sk-PERSONAL-KEY" not in content


def test_connections_add_rejects_unknown_provider(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["connections", "add", "unknown"],
    )

    assert result.exit_code != 0
    assert 'Unknown provider "unknown".' in result.output


def test_connections_add_rejects_empty_name(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "connections",
            "add",
            "openai",
            "--name",
            "   ",
        ],
    )

    assert result.exit_code != 0
    assert "Connection name cannot be empty." in result.output


def test_connections_list_shows_configured_credentials(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    from bindai_connections import ConnectionManifest

    ConnectionManifest(
        tmp_path / ".bindai" / "connections.toml",
    ).add(
        "work",
        "openai",
    )

    class FakeKeyring:
        def get_password(self, service, username):
            assert username == "work"
            return "secret-key"

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        ["connections", "list"],
    )

    assert result.exit_code == 0
    assert "work" in result.stdout
    assert "openai" in result.stdout
    assert "Configured" in result.stdout
    assert "secret-key" not in result.stdout


def test_connections_list_shows_missing_credentials(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    from bindai_connections import ConnectionManifest

    ConnectionManifest(
        tmp_path / ".bindai" / "connections.toml",
    ).add(
        "work",
        "openai",
    )

    class FakeKeyring:
        def get_password(self, service, username):
            assert username == "work"
            return None

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        ["connections", "list"],
    )

    assert result.exit_code == 0
    assert "work" in result.stdout
    assert "openai" in result.stdout
    assert "Missing" in result.stdout


def test_connections_list_empty_manifest(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["connections", "list"],
    )

    assert result.exit_code == 0
    assert "BindAI Connections" in result.stdout


def test_connections_remove_deletes_credential_and_manifest(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    from bindai_connections import ConnectionManifest

    manifest = ConnectionManifest(
        tmp_path / ".bindai" / "connections.toml",
    )
    manifest.add("work", "openai")

    stored: dict[tuple[str, str], str] = {
        ("bindai", "work"): "secret-key",
    }

    class FakeKeyring:
        def get_password(self, service, username):
            return stored.get((service, username))

        def delete_password(self, service, username):
            stored.pop((service, username), None)

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        ["connections", "remove", "work"],
    )

    assert result.exit_code == 0
    assert 'Connection "work" removed.' in result.stdout

    assert stored == {}
    assert manifest.list() == []


def test_connections_remove_allows_shared_provider_connections(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    from bindai_connections import ConnectionManifest

    manifest = ConnectionManifest(
        tmp_path / ".bindai" / "connections.toml",
    )
    manifest.add("work", "openai")
    manifest.add("personal", "openai")

    stored: dict[tuple[str, str], str] = {
        ("bindai", "work"): "work-secret",
        ("bindai", "personal"): "personal-secret",
    }

    class FakeKeyring:
        def get_password(self, service, username):
            return stored.get((service, username))

        def delete_password(self, service, username):
            stored.pop((service, username), None)

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        ["connections", "remove", "work"],
    )

    assert result.exit_code == 0
    assert 'Connection "work" removed.' in result.stdout

    assert ("bindai", "work") not in stored
    assert stored[("bindai", "personal")] == "personal-secret"

    remaining = manifest.list()

    assert len(remaining) == 1
    assert remaining[0].name == "personal"


def test_connections_remove_rejects_missing_connection(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["connections", "remove", "missing"],
    )

    assert result.exit_code != 0
    assert 'Connection "missing" not found.' in result.output