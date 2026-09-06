from bindai_connections.connection import Connection


class DummyConnection(Connection):
    def __init__(self):
        self.connected = False

    @property
    def name(self) -> str:
        return "test"

    def connect(self) -> None:
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def send(self, payload):
        if not self.connected:
            raise RuntimeError("Connection is not active.")
        return payload


def test_connection_lifecycle():
    connection = DummyConnection()

    assert connection.name == "test"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    assert connection.send({"message": "hello"}) == {"message": "hello"}

    connection.disconnect()
    assert not connection.is_connected()


def test_connection_requires_active_state():
    connection = DummyConnection()

    try:
        connection.send("hello")
    except RuntimeError as exc:
        assert str(exc) == "Connection is not active."
    else:
        raise AssertionError("Expected RuntimeError")

