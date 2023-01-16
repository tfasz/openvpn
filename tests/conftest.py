# pylint: disable=redefined-outer-name
"""Location for pytest fixtures."""
import os
import pytest
from pki_config import PkiConfig
from server_config import ServerConfig
from tests import PKI_BIN_DIR, sample_dir, temp_dir, rm_tree

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Run cleanup logic at end of all tests"""
    def clear_temp():
        """"Clear temp directory"""
        rm_tree(temp_dir)
    request.addfinalizer(clear_temp)

@pytest.fixture(scope='function')
def get_sample_dir():
    """Get directory with sample test data"""
    return sample_dir

@pytest.fixture(scope='function')
def get_temp_dir():
    """Get directory to use as temp working directory during tests. This is cleaned up between and after tests."""
    rm_tree(temp_dir)
    os.makedirs(temp_dir)
    return temp_dir

@pytest.fixture(scope='function')
def server_config(get_temp_dir):
    """Get server configuration used for much of our testing."""
    config = ServerConfig(get_temp_dir, "vpn.example.com", 1194, True, ["192.168.0.2","192.168.0.3"])
    config.save()
    return config

@pytest.fixture(scope='function')
def pki_config(server_config):
    """Get server and pki configuration used for much of our testing."""
    config = PkiConfig(server_config.vpn_dir, PKI_BIN_DIR)
    config.init()
    return config
