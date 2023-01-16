"""Output client config ovpn file contents for an existing user"""
import os
from ovpn_util import load_config, read_file, read_x509, ValidationException
from pki_config import PkiConfig

class ClientConfig:
    """Load config and generate client ovpn file contents"""
    def __init__(self, vpn_dir, pki_bin_dir):
        self.vpn_dir = vpn_dir
        self.vpn_config = load_config(vpn_dir)
        self.pki_config = PkiConfig(vpn_dir, pki_bin_dir)

    def get_client_key_file(self, name):
        """Get the path to the client key file."""
        client_key_file = f"{self.pki_config.pki_dir}/private/{name}.key"
        return client_key_file

    def generate(self, client_key_file, name):
        """Create a client cert if it doesn't yet exist"""
        if not os.path.exists(client_key_file):
            self.pki_config.gen_client(name)

    def get(self, name):
        """Get the clients config as a string"""
        client_key_file = self.get_client_key_file(name)
        self.generate(client_key_file, name)

        # Now that we have a client created, generate the OVPN config file
        data = self.vpn_config
        data["client_key"] = read_file(client_key_file)
        data["client_cert"] = read_x509(f"{self.pki_config.pki_dir}/issued/{name}.crt")
        data["ca_cert"] = read_file(f"{self.pki_config.pki_dir}/ca.crt")
        data["tls_crypt_key"] = read_file(f"{self.pki_config.pki_dir}/tls-crypt.key")
        return data

    def revoke(self, name):
        """Revoke a client's certificate"""
        client_key_file = self.get_client_key_file(name)
        if not os.path.exists(client_key_file):
            raise ValidationException(f"Unable to find client key for \"{name}\".")

        # revoke client and re-generate the CRL
        self.pki_config.revoke_client(name)
