# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
import pytest
from pki_config import PkiConfig
from ovpn_util import read_file
from tests import PKI_BIN_DIR, temp_pki_dir, test_dir, read_expected_output, rm_tree

def test_pki_error():
    rm_tree(temp_pki_dir)
    config = PkiConfig(test_dir, temp_pki_dir, PKI_BIN_DIR)
    with pytest.raises(Exception):
        config.exec_pki("invalid-argument")

def test_pki_config():
    rm_tree(temp_pki_dir)
    config = PkiConfig(test_dir, temp_pki_dir, PKI_BIN_DIR)
    config.init()
    assert read_file(os.path.join(test_dir, "easyrsa-vars")) == read_expected_output("easyrsa-vars")
    assert read_file(os.path.join(test_dir, "crl.pem")) == read_file(os.path.join(temp_pki_dir, "crl.pem"))

def test_pki_config_client():
    """Verify we can generate a client config."""
    config = PkiConfig(test_dir, temp_pki_dir, PKI_BIN_DIR)
    config.gen_client("test")
    assert os.path.exists(os.path.join(temp_pki_dir, "issued/test.crt"))
    assert os.path.exists(os.path.join(temp_pki_dir, "private/test.key"))
