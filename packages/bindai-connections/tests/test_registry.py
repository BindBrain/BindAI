import pytest
from bindai_connections.connection import Connection
from bindai_connections.registry import ConnectionRegistry


class DummyConnection(Connection):
    @property
    def name(self) -> str:
        return "dummy"

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def is_connected(self) -> bool:
        return True

    def send(self, payload):
        return payload


def test_registry_register_and_provider():
    ConnectionRegistry.register("dummy", DummyConnection)

    assert ConnectionRegistry.provider("dummy") is DummyConnection


def test_registry_names():
    ConnectionRegistry.register("dummy", DummyConnection)

    assert "dummy" in ConnectionRegistry.names()


def test_registry_rejects_empty_name():
    with pytest.raises(ValueError):
        ConnectionRegistry.register("", DummyConnection)


def test_registry_rejects_unknown_connection():
    with pytest.raises(KeyError):
        ConnectionRegistry.provider("missing")


def test_webhook_connection_is_registered():
    from bindai_connections import WebhookConnection

    assert ConnectionRegistry.provider("webhook") is WebhookConnection
