# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from server_config import ServerConfig
from ovpn_util import load_json
from tests import get_expected_output_file

def test_server_config(get_temp_dir):
    # Generate the JSON data and validate
    config = ServerConfig(get_temp_dir, "vpn.example.com", 1194, True, ["192.168.0.2","192.168.0.3"])
    assert config.render() == load_json(get_expected_output_file("test-server-conf.json"))

def test_server_config_mtu(get_temp_dir):
    config = ServerConfig(get_temp_dir, "vpn.example.com", 1194, True, ["192.168.0.2","192.168.0.3"], mtu=1400)
    assert "tun-mtu 1400" in config.render()
