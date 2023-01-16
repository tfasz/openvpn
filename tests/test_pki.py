# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
import pytest
from pki_config import PkiConfig
from ovpn_util import read_file
from tests import PKI_BIN_DIR, read_expected_output, read_temp_file

def test_pki_error(server_config):
    config = PkiConfig(server_config.vpn_dir, PKI_BIN_DIR)
    config.pki_dir = "/tmp/invalid-dir"
    with pytest.raises(Exception):
        config.exec_pki("invalid-argument")

def test_pki_config(server_config):
    config = PkiConfig(server_config.vpn_dir, PKI_BIN_DIR)
    config.init()
    assert read_temp_file("easyrsa-vars") == read_expected_output("easyrsa-vars")
    assert read_temp_file("crl.pem") == read_file(os.path.join(config.pki_dir, "crl.pem"))

def test_pki_config_client(server_config):
    """Verify we can generate a client config."""
    config = PkiConfig(server_config.vpn_dir, PKI_BIN_DIR)
    config.init()
    config.gen_client("test")
    assert os.path.exists(os.path.join(config.pki_dir, "issued/test.crt"))
    assert os.path.exists(os.path.join(config.pki_dir, "private/test.key"))
