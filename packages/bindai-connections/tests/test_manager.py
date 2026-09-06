from bindai_connections import ConnectionManager, WebhookConnection


def test_connection_manager_add_and_get():
    manager = ConnectionManager()
    connection = WebhookConnection("https://example.com/webhook")

    assert manager.add(connection) is manager
    assert manager.get("webhook") is connection
    assert manager.contains("webhook")
    assert manager.names() == ["webhook"]
    assert manager.size() == 1


def test_connection_manager_connect_and_disconnect():
    manager = ConnectionManager()
    connection = WebhookConnection("https://example.com/webhook")
    manager.add(connection)

    manager.connect("webhook")
    assert connection.is_connected()

    manager.disconnect("webhook")
    assert not connection.is_connected()


def test_connection_manager_remove_disconnects_active_connection():
    manager = ConnectionManager()
    connection = WebhookConnection("https://example.com/webhook")
    manager.add(connection)
    manager.connect("webhook")

    manager.remove("webhook")

    assert not connection.is_connected()
    assert not manager.contains("webhook")
    assert manager.size() == 0


def test_connection_manager_disconnect_all_and_clear():
    manager = ConnectionManager()
    first = WebhookConnection("https://example.com/one")
    second = WebhookConnection("https://example.com/two")

    manager.add(first).add(second)
    manager.connect("webhook")

    # The manager keys connections by connection.name, so adding two
    # webhook connections replaces the first one.
    assert manager.size() == 1

    manager.disconnect_all()
    assert not second.is_connected()

    manager.clear()
    assert manager.size() == 0


def test_connection_manager_unknown_connection():
    manager = ConnectionManager()

    try:
        manager.get("missing")
    except KeyError as exc:
        assert str(exc) == '"Connection \'missing\' is not managed."'
    else:
        raise AssertionError("Expected KeyError")