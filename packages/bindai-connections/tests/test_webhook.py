from bindai_connections import WebhookConnection


def test_webhook_connection_lifecycle():
    connection = WebhookConnection("https://example.com/webhook")

    assert connection.name == "webhook"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_webhook_connection_rejects_empty_url():
    try:
        WebhookConnection("")
    except ValueError as exc:
        assert str(exc) == "Webhook URL cannot be empty."
    else:
        raise AssertionError("Expected ValueError")


def test_webhook_connection_rejects_invalid_timeout():
    try:
        WebhookConnection("https://example.com/webhook", timeout=0)
    except ValueError as exc:
        assert str(exc) == "Webhook timeout must be greater than zero."
    else:
        raise AssertionError("Expected ValueError")


def test_webhook_connection_requires_active_state():
    connection = WebhookConnection("https://example.com/webhook")

    try:
        connection.send({"message": "hello"})
    except RuntimeError as exc:
        assert str(exc) == "Connection is not active."
    else:
        raise AssertionError("Expected RuntimeError")

def test_webhook_connection_sends_json_payload(monkeypatch):
    connection = WebhookConnection("https://example.com/webhook")
    connection.connect()

    class DummyResponse:
        status = 200

        def read(self):
            return b'{"ok": true}'

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.method
        captured["body"] = request.data
        captured["content_type"] = request.headers["Content-type"]
        captured["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr(
        "bindai_connections.webhook.urlopen",
        fake_urlopen,
    )

    result = connection.send({"message": "hello"})

    assert captured["url"] == "https://example.com/webhook"
    assert captured["method"] == "POST"
    assert captured["body"] == b'{"message": "hello"}'
    assert captured["content_type"] == "application/json"
    assert captured["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"ok": true}',
    }