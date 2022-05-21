# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
from click.testing import CliRunner
from ovpn_initpki import gen_pki
from tests import test_dir, rm_tree

def test_pki_cli():
    pki_dir = os.path.join(test_dir, "temp/pki-config")
    rm_tree(pki_dir)
    result = CliRunner().invoke(gen_pki, ["-D", test_dir, "-p", pki_dir, "-b", "/usr/share/easy-rsa"])
    assert result.exit_code == 0
    assert os.path.exists(os.path.join(pki_dir, "ca.crt"))
    assert os.path.exists(os.path.join(pki_dir, "crl.pem"))
    assert os.path.exists(os.path.join(pki_dir, "private/ca.key"))
    assert os.path.exists(os.path.join(pki_dir, "private/vpn.example.com.key"))
    assert os.path.exists(os.path.join(pki_dir, "tls-crypt.key"))

# Test with no valid config present
def test_pki_cli_no_config():
    invalid_test_dir = os.path.join(test_dir, "temp/no-config")
    pki_dir = os.path.join(test_dir, "temp/pki-config")
    rm_tree(pki_dir)
    result = CliRunner().invoke(gen_pki, ["-D", invalid_test_dir, "-p", pki_dir, "-b", "/usr/share/easy-rsa"])
    assert result.exit_code == 1
