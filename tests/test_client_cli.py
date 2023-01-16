# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from click.testing import CliRunner
from ovpn_getclient import get_client
from ovpn_revokeclient import revoke_client

def test_client_cli(pki_config):
    result = CliRunner().invoke(get_client, args=["-D", pki_config.vpn_dir, "-b", "/usr/share/easy-rsa", "test"])
    assert result.exit_code == 0

def test_client_cli_no_pki():
    result = CliRunner().invoke(get_client, ["-D", "/tmp/invalid-dir", "-b", "/usr/share/easy-rsa", "test"])
    assert result.exit_code == 1

def test_revoke_client_cli_no_user(pki_config):
    result = CliRunner().invoke(revoke_client, ["-D", pki_config.vpn_dir, "-b", "/usr/share/easy-rsa", "fake-user"])
    assert result.exit_code == 1

def test_revoke_client_cli_no_pki():
    result = CliRunner().invoke(revoke_client, ["-D", "/tmp/invalid-dir", "-b", "/usr/share/easy-rsa", "test"])
    assert result.exit_code == 1
