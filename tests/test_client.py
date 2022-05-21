# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
import pytest
from client_config import ClientConfig
from pki_config import PkiConfig
from ovpn_util import load_json, ValidationException
from tests import static_pki_dir, temp_pki_dir, test_dir, PKI_BIN_DIR, get_expected_output_file, rm_tree

def test_get_client_config():
    expected_json = load_json(get_expected_output_file("test-client-conf.json"))
    client_config = ClientConfig(test_dir, static_pki_dir, PKI_BIN_DIR)
    data = client_config.get("test")
    assert data == expected_json

def test_get_client_no_pki():
    with pytest.raises(ValidationException):
        client_config = ClientConfig(test_dir, os.path.join(test_dir, "fake-pki-dir"), PKI_BIN_DIR)
        client_config.get("test")

def test_revoke_client_config_fake_user():
    """Ensure revoking a fake user throws exception."""
    client_config = ClientConfig(test_dir, static_pki_dir, PKI_BIN_DIR)
    with pytest.raises(ValidationException):
        client_config.revoke("fake-user")

def test_revoke_client_config():
    rm_tree(temp_pki_dir)
    # Create PKI
    pki = PkiConfig(test_dir, temp_pki_dir, PKI_BIN_DIR)
    pki.init()
    # Create client
    client = ClientConfig(test_dir, temp_pki_dir, PKI_BIN_DIR)
    client.get("test")
    assert os.path.exists(os.path.join(temp_pki_dir, "private/test.key"))
    # Revoke client
    client.revoke("test")
    assert not os.path.exists(os.path.join(temp_pki_dir, "private/test.key"))
    assert os.path.exists(os.path.join(test_dir, "crl.pem"))
