# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
import pytest
from client_config import ClientConfig
from ovpn_util import load_config, ValidationException
from tests import PKI_BIN_DIR

def test_get_client_config(pki_config):
    client = ClientConfig(pki_config.vpn_dir, PKI_BIN_DIR)
    data = client.get("test")
    assert os.path.exists(os.path.join(pki_config.pki_dir, "private/test.key"))

    config = load_config(pki_config.vpn_dir, "config.json")
    assert data["common_name"] == config["common_name"]
    assert data["port"] == config["port"]
    assert data["proto"] == config["proto"]
    assert data["dns_servers"] == config["dns_servers"]
    assert data["slack_notify_url"] == config["slack_notify_url"]

def test_get_client_no_pki(pki_config):
    client_config = ClientConfig(pki_config.vpn_dir, PKI_BIN_DIR)
    client_config.pki_config.pki_dir = "/tmp/invalid-dir"
    with pytest.raises(ValidationException):
        client_config.get("test")

def test_revoke_client_config_fake_user(pki_config):
    """Ensure revoking a fake user throws exception."""
    client_config = ClientConfig(pki_config.vpn_dir, PKI_BIN_DIR)
    with pytest.raises(ValidationException):
        client_config.revoke("fake-user")

def test_revoke_client_config(pki_config):
    # Create client
    client = ClientConfig(pki_config.vpn_dir, PKI_BIN_DIR)
    client.get("test")
    assert os.path.exists(os.path.join(pki_config.pki_dir, "private/test.key"))
    # Revoke client
    client.revoke("test")
    assert not os.path.exists(os.path.join(pki_config.pki_dir, "private/test.key"))
