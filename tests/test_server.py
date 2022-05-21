# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
from server_config import ServerConfig
from ovpn_util import load_json
from tests import test_dir, get_expected_output_file

def test_server_config():
    expected_json = load_json(get_expected_output_file("test-server-conf.json"))

    # Generate the JSON data and validate
    config = ServerConfig(test_dir, "vpn.example.com", 1194, True, ["192.168.0.2","192.168.0.3"])
    assert config.render() == expected_json
