# pylint: disable=import-error,missing-function-docstring,missing-module-docstring,missing-class-docstring
from unittest.mock import patch
from click.testing import CliRunner
import slack_sdk
from ovpn_notify import notify

class MockResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

def test_notify_cli(server_config):
    with patch.object(slack_sdk.webhook.WebhookClient, 'send', return_value=MockResponse(200, "Ok")):
        result = CliRunner().invoke(notify, ["-D", server_config.vpn_dir, "-e", "client-connect", "-c", "test"])
        print(f"{result.output}")
        assert result.exit_code == 0
        assert result.output == "Slack notification status #200:Ok\n"

def test_notify_cli_disconnect(server_config):
    with patch.object(slack_sdk.webhook.WebhookClient, 'send', return_value=MockResponse(200, "Ok")):
        result = CliRunner().invoke(notify, ["-D", server_config.vpn_dir, "-e", "client-disconnect", "-c", "test", "-d", "60",
                                             "-s", "100", "-r", "200"])
        print(f"{result.output}")
        assert result.exit_code == 0
        assert result.output == "Slack notification status #200:Ok\n"
