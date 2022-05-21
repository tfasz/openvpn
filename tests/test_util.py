# pylint: disable=import-error,missing-function-docstring,missing-module-docstring
import os.path
import pytest
from ovpn_util import load_config, read_file, read_x509, render_template, save_config
from tests import test_dir, get_expected_output_file

def test_load_config():
    config = load_config(test_dir, "sample-config.json")
    assert config["common_name"] == "vpn.example.com"
    assert config["dns_servers"][0] == "192.168.0.2"

def test_read_file():
    assert read_file(get_expected_output_file("test.txt")) == "FOO"

def test_read_x509():
    file_cert = read_x509(os.path.join(test_dir,"test-pki/issued/test.crt"))
    assert file_cert == TEST_CERT

def test_read_x509_error():
    with pytest.raises(Exception):
        read_x509(os.path.join(test_dir,"test-pki/issued/bad-cert.crt"))

def test_save_config():
    config_file_name = "temp/config.json"
    data = {}
    data["foo"] = "bar"
    save_config(data, test_dir, config_file_name)
    config = load_config(test_dir, config_file_name)
    assert config == data

def test_write_json():
    config_file_name = "temp/config.json"
    data = {}
    data["foo"] = "bar"
    save_config(data, test_dir, config_file_name)
    config = load_config(test_dir, config_file_name)
    assert config == data

def test_render_template():
    data = load_config(test_dir, "config.json")
    data["client_key"] = "foo-key"
    data["client_cert"] = "foo-cert"
    data["ca_cert"] = "foo-ca-cert"
    data["tls_crypt_key"] = "secret"
    output = render_template("client.ovpn.j2", data)
    assert output == CLIENT_CONF

TEST_CERT="""-----BEGIN CERTIFICATE-----
MIICgjCCAWqgAwIBAgIRAJmMFpXknQRwoyXc7wjcFd0wDQYJKoZIhvcNAQELBQAw
EzERMA8GA1UEAwwIQ2hhbmdlTWUwHhcNMjIwNjAxMDEzOTAzWhcNMjcwNTMxMDEz
OTAzWjAPMQ0wCwYDVQQDDAR0ZXN0MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE
0mPksVQhTEGJgDLZrEgPXBHId56idPdYchonyFc7g2bqL+DUCUYpIGAZAq3FQ4tB
btU6MZaXwwWthSXCQJazD6OBnzCBnDAJBgNVHRMEAjAAMB0GA1UdDgQWBBT+7PzR
bopkzrR9QepXubrV2lNKATBOBgNVHSMERzBFgBQ7clpBhsAGsLHAOen0YIEhYb4z
a6EXpBUwEzERMA8GA1UEAwwIQ2hhbmdlTWWCFDHE0iDdG+hrx4XeLAw+MtErEBcD
MBMGA1UdJQQMMAoGCCsGAQUFBwMCMAsGA1UdDwQEAwIHgDANBgkqhkiG9w0BAQsF
AAOCAQEA6uHgTZyXt9SpFuCqW93BG1G2jZFnGZyzCkA+J70BjRlwIwB6shOEYrpC
Efe9W1T2qAbRadEtlaQyFDYRryW3sX0ggzOyo4We0carMqoFdmNRKYj+EUKJ0snG
IZs4okmUp7jRkK8iWGYKFlh84oJkanf3gPnmAa36t+AHZIVqdkKzaIiO99bxblRa
HV4Peau6to8iyaB5piuW/4QXCrniikv9U8n50/G7AChuSIlEBMpi2IEXOxjq4BDK
Rga6gKHATk3SAQXLUurqF3pzKgDCNPO5nYQXr0LHZWamFDUSSUu2BpAdXZ0ir56w
/Kt8IuRmKLscG6/56xo7EgZeHdxgrw==
-----END CERTIFICATE-----
"""

CLIENT_CONF="""client
nobind
dev tun
auth SHA256
remote-cert-tls server
remote vpn.example.com 1194 tcp4
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
