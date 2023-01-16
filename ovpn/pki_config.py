"""Manage the PKI config for the VPN server"""
import os
import shutil
from subprocess import Popen, PIPE
from ovpn_util import load_config, render_template, write_file, ValidationException

class PkiConfig:
    """Manage PKI config for VPN server"""
    def __init__(self, vpn_dir, pki_bin_dir):
        self.vpn_dir = vpn_dir
        self.pki_dir = os.path.join(self.vpn_dir, "pki")
        self.easyrsa_vars_file = os.path.join(self.vpn_dir, "vars")
        self.easyrsa_bin = os.path.join(pki_bin_dir, "easyrsa")
        self.tls_crypt_key = os.path.join(self.pki_dir, "tls-crypt.key")

    def exec(self, cmd):
        """Execute command with proper easyrsa environment variables set."""
        env = {"EASYRSA_PKI":self.pki_dir}
        args = cmd.split()
        with Popen(args, env=env, stdout=PIPE,  stderr=PIPE) as proc:
            proc.communicate()
            if proc.returncode > 0:
                raise Exception(f"Command \"{cmd}\" failed with return code #{proc.returncode}.")

    def exec_pki(self, cmd):
        """Execute easyrsa command with proper environment variables set"""
        self.exec(f"{self.easyrsa_bin} {cmd}")

    def init(self):
        """
        Initialize the PKI for our VPN server using the relevant config. This will build the
        folder structure, create a certificate authority to sign certs, generate the server certs,
        and create a secret we will use for TLS encryption of our VPN control channel.
        """
        config = load_config(self.vpn_dir)
        # Write vars file to ensure key types are configured correctly
        write_file(self.easyrsa_vars_file, render_template("vars.j2", config))

        # Provides a sufficient warning before erasing pre-existing files
        self.exec_pki("init-pki")

        # Generate server CA - don't set password on CA to keep it simple. Anyone with
        # access to this container will be able to generate client credentials.
        self.exec_pki("--batch build-ca nopass")

        # Create our secret for the TLS crypt key
        self.exec(f"/usr/sbin/openvpn --genkey secret {self.tls_crypt_key}")

        # For a server key with a password, manually init; this is autopilot
        self.exec_pki(f"--batch build-server-full {config['common_name']} nopass")

        # Init CRL
        self.gen_crl()

    def gen_crl(self):
        """Generate the CRL for the server"""
        # While the EASYRSA_VARS_FILE variable is set the CRL doesn't get set to the correct expiration without
        # explicitly including it on the CLI. You can view the CRL details with: openssl crl -text -noout -in crl.pem
        self.exec_pki("gen-crl")

        # copy updated CRL from PKI dir to the VPN dir and make readable by everyone so the OpenVPN process
        # can read it
        shutil.copy(os.path.join(self.pki_dir, "crl.pem"), self.vpn_dir)
        os.chmod(os.path.join(self.vpn_dir, "crl.pem"), 0o644)

    def ensure_init(self):
        """Ensure that the PKI directory exists"""
        if not os.path.exists(self.pki_dir):
            raise ValidationException("PKI config directory does not exist - have you run ovpn_initpki?")

    def gen_client(self, name):
        """Generate a client certificate for name"""
        self.ensure_init()
        self.exec_pki(f"--batch build-client-full {name} nopass")

    def revoke_client(self, name):
        """Revoke the client certificate for name"""
        self.ensure_init()
        self.exec_pki(f"--batch revoke {name}")
        self.gen_crl()
