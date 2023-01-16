# pylint: disable=import-error,missing-function-docstring,missing-module-docstring,missing-class-docstring
from notify_handler import get_duration_text, NotificationHandler

class MockHandler():
    def __init__(self):
        self.msg = None

    def send(self, msg):
        self.msg = msg

def test_get_duration_text_seconds():
    assert get_duration_text(55) == "55s"
    assert get_duration_text(90) == "90s"

def test_get_duration_text_minutes():
    assert get_duration_text(120) == "2m"
    assert get_duration_text(240) == "4m"
    assert get_duration_text(3600) == "60m"

def test_get_duration_text_hours():
    assert get_duration_text(7200) == "2h"
    assert get_duration_text(7201) == "2h"
    assert get_duration_text(14400) == "4h"
    assert get_duration_text(129600) == "36h"

def test_handler_connect(server_config):
    mock = MockHandler()
    handler = NotificationHandler(server_config.vpn_dir, "client-connect", "2022-01-01 12:00:00", None, "1.1.1.1", "test", None, None)
    handler.set_handler(mock)
    handler.send()
    assert mock.msg == "User test connected @ 2022-01-01 12:00:00 from 1.1.1.1"

def test_handler_disconnect(server_config):
    mock = MockHandler()
    handler = NotificationHandler(server_config.vpn_dir, "client-disconnect", "2022-01-01 12:00:00", 120, "1.1.1.1", "test", 100, 200)
    handler.set_handler(mock)
    handler.send()
    assert mock.msg == "User test disconnected after 2m, sent: 100, received: 200"

def test_handler_unknown_event(server_config):
    mock = MockHandler()
    handler = NotificationHandler(server_config.vpn_dir, "unknown-event", "2022-01-01 12:00:00", 120, "1.1.1.1", "test", 100, 200)
    handler.set_handler(mock)
    handler.send()
    assert mock.msg is None
