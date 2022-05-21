# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from click.testing import CliRunner
from ovpn_genconfig import gen_server
from tests import temp_dir, read_expected_output, read_temp_file

def test_server_cli():
    result = CliRunner().invoke(gen_server, ["-t", "-d", "192.168.0.2", "-d", "192.168.0.3", "-D", temp_dir, "vpn.example.com"])
    print(f"{result.output}")
    assert result.exit_code == 0
    assert read_temp_file("server.conf") == read_expected_output("test-server.conf")

def test_server_cli_slack():
    result = CliRunner().invoke(gen_server, ["-t", "-d", "192.168.0.2", "-d", "192.168.0.3", "-D", temp_dir,
                                             "-s", "https://hooks.slack.com/foo", "vpn.example.com"])
    print(f"{result.output}")
    assert result.exit_code == 0
    assert read_temp_file("server.conf") == read_expected_output("test-server-slack.conf")
