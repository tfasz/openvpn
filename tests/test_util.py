# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
from datetime import datetime

import pytest
from ovpn_util import load_config, read_file, read_x509, read_x509_end_date, render_template, save_config
from tests import get_expected_output_file

def test_load_config(get_sample_dir):
    config = load_config(get_sample_dir, "config.json")
    assert config["common_name"] == "vpn.example.com"
    assert config["dns_servers"][0] == "1.1.1.1"

def test_read_file():
    assert read_file(get_expected_output_file("foo.txt")) == "FOO"

def test_read_x509(get_sample_dir):
    file_cert = read_x509(os.path.join(get_sample_dir, "vpn.example.com.crt"))
    assert file_cert == TEST_CERT

def test_read_x509_error(get_sample_dir):
    with pytest.raises(Exception):
        read_x509(os.path.join(get_sample_dir, "bad-cert.crt"))

def test_read_x509_end_date(get_sample_dir):
    end_date = read_x509_end_date(os.path.join(get_sample_dir, "vpn.example.com.crt"))
    assert end_date == datetime(2025, 4, 19, 22, 17, 51)

def test_save_config(get_temp_dir):
    data = {}
    data["foo"] = "bar"
    save_config(data, get_temp_dir, "config.json")
    config = load_config(get_temp_dir, "config.json")
    assert config == data

def test_render_template(get_sample_dir):
    data = load_config(get_sample_dir, "config.json")
    data["client_key"] = "foo-key"
    data["client_cert"] = "foo-cert"
    data["ca_cert"] = "foo-ca-cert"
    data["tls_crypt_key"] = "secret"
    output = render_template("client.ovpn.j2", data)
    assert output == CLIENT_CONF

TEST_CERT="""-----BEGIN CERTIFICATE-----
MIIDejCCAmKgAwIBAgIRAJkR2Pi5GXpWvq9Hpv+VZLIwDQYJKoZIhvcNAQELBQAw
FjEUMBIGA1UEAwwLRWFzeS1SU0EgQ0EwHhcNMjMwMTE1MjIxNzUxWhcNMjUwNDE5
MjIxNzUxWjAaMRgwFgYDVQQDDA92cG4uZXhhbXBsZS5jb20wggEiMA0GCSqGSIb3
DQEBAQUAA4IBDwAwggEKAoIBAQC0J9xBeofEtQ7zdpDtc4XdpzaFeATjI4keP7sP
tZAq1i76lXC7RyjEUSpQ/es4FuGMdlh0EHQONMbW1mREhV+i8hd24HtUacJbYNg+
jnPsOCqzI/3jTXcD7YJmVRUduCB8pSMGr5Gz/6JPSOsK18JWMvu7Z3J4G30u8+Wi
34OSY1dw5KSkjbwX9AeJ2h3FtrmL1LIJ2OB/JZE3a3uEod9d78me/hTeBaubtAWO
+1a4TjQ2R3s+EY3/3olKbYXQMJzPmmaCrt+52/vYLgeb3zspOVLWPdcgpYXxilfO
/wj2m/Xs4GWiG71L4myq4BEokAXbG4OqyeWDrCKnFtZgZo9nAgMBAAGjgb4wgbsw
CQYDVR0TBAIwADAdBgNVHQ4EFgQUYpD8tWaMFnBE/uvhrcTj3mvG2WowUQYDVR0j
BEowSIAUvAyp2FlB7fPYvp7yDWnrV+F/6WehGqQYMBYxFDASBgNVBAMMC0Vhc3kt
UlNBIENBghQ2PUlq2kqvZ1418AMQ2XzZKsyDsjATBgNVHSUEDDAKBggrBgEFBQcD
ATALBgNVHQ8EBAMCBaAwGgYDVR0RBBMwEYIPdnBuLmV4YW1wbGUuY29tMA0GCSqG
SIb3DQEBCwUAA4IBAQBr+B9bkKFjfm/OTZNtl2RqBcIlbpGLRh+77BtfnxKtoJdP
9dvpndsnMui1aR0SVgOXMlwEwxrrOMv3+GPdq3BQ5gATSOWBJo1IhgF+ZLCSpA9d
P1PCqtfLQOTxLYwnYFBFSRdQH0ttbmiNAOAOFNGn9sGPNtBdLgTbu8mJoPByK2if
yLaxfzk7QjiOXa5fFEwVb7RygCex4r12RTB4q/VZ8X9eoyDCSYI8rZG5kzigLQLS
GD8h5uKXKeq5sW1M7Bn5qtpADdZhzo3B9OhbqpL/jTucZ3bOREMvmcEqbaCNRf0I
NSBCu7amPJrHrlXxHGnKsHGn6A9HdSuPeaUBMTSb
-----END CERTIFICATE-----
"""

CLIENT_CONF="""client
nobind
dev tun
auth SHA256
remote-cert-tls server
remote vpn.example.com 1194 udp4
verify-x509-name vpn.example.com name
tls-client
tun-mtu 1500
verb 3
<ca>
foo-ca-cert
</ca>
<cert>
foo-cert
</cert>
<key>
foo-key
</key>
<tls-crypt>
secret
</tls-crypt>"""
