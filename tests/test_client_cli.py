# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from click.testing import CliRunner
from ovpn_getclient import get_client
from ovpn_revokeclient import revoke_client
from tests import test_dir, static_pki_dir, read_expected_output

def test_client_cli():
    result = CliRunner().invoke(get_client, ["-D", test_dir, "-p", static_pki_dir, "test"])
    assert result.exit_code == 0
    assert result.output == read_expected_output("test-client.conf")

def test_client_cli_no_pki():
    result = CliRunner().invoke(get_client, ["-D", test_dir, "-p", "/tmp/fake-pki-dir", "test"])
    assert result.exit_code == 1

def test_revoke_client_cli_no_pki():
    result = CliRunner().invoke(revoke_client, ["-D", test_dir, "-p", "/tmp/fake-pki-dir", "test"])
    assert result.exit_code == 1

def test_revoke_client_cli_no_user():
    result = CliRunner().invoke(revoke_client, ["-D", test_dir, "-p", static_pki_dir, "fake-user"])
    assert result.exit_code == 1
