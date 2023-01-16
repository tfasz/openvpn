# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
from click.testing import CliRunner
from ovpn_initpki import gen_pki

def test_pki_cli(server_config):
    result = CliRunner().invoke(gen_pki, ["-D", server_config.vpn_dir, "-b", "/usr/share/easy-rsa"])
    pki_dir = os.path.join(server_config.vpn_dir, "pki")
    assert result.exit_code == 0
    assert os.path.exists(os.path.join(pki_dir, "ca.crt"))
    assert os.path.exists(os.path.join(pki_dir, "crl.pem"))
    assert os.path.exists(os.path.join(pki_dir, "private/ca.key"))
    assert os.path.exists(os.path.join(pki_dir, "private/vpn.example.com.key"))
    assert os.path.exists(os.path.join(pki_dir, "tls-crypt.key"))

# Test with no valid config present
def test_pki_cli_no_config(server_config):
    invalid_config_dir = os.path.join(server_config.vpn_dir, "invalid_dir")
    result = CliRunner().invoke(gen_pki, ["-D", invalid_config_dir, "-b", "/usr/share/easy-rsa"])
    assert result.exit_code == 1
