# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os

from click.testing import CliRunner
from ovpn_genconfig import gen_server
from ovpn_util import read_file
from tests import read_expected_output

def test_server_cli(get_temp_dir):
    result = CliRunner().invoke(gen_server, ["-t", "-d", "192.168.0.2", "-d", "192.168.0.3", "-D", get_temp_dir, "vpn.example.com"])
    print(f"{result.output}")
    assert result.exit_code == 0
    assert read_file(os.path.join(get_temp_dir, "server.conf")) == read_expected_output("test-server.conf")

def test_server_cli_slack(get_temp_dir):
    result = CliRunner().invoke(gen_server, ["-t", "-d", "192.168.0.2", "-d", "192.168.0.3", "-D", get_temp_dir,
                                             "-s", "https://hooks.slack.com/foo", "vpn.example.com"])
    print(f"{result.output}")
    assert result.exit_code == 0
    assert read_file(os.path.join(get_temp_dir, "server.conf")) == read_expected_output("test-server-slack.conf")
