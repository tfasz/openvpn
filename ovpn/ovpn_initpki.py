#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter
"""CLI command for initializing the PKI config of the VPN server"""
import sys
import click
from pki_config import PkiConfig
from ovpn_util import ValidationException

@click.command()
@click.option("-D", "--vpndir", envvar='OPENVPN', help="OpenVPN config directory")
@click.option("-p", "--pkidir", envvar='EASYRSA_PKI', help="PKI config directory")
@click.option("-b", "--bindir", envvar='EASYRSA', help="PKI binary directory")
def gen_pki(vpndir, pkidir, bindir):
    """Generate VPN PKI"""
    try:
        pki_config = PkiConfig(vpndir, pkidir, bindir)
        pki_config.init()
    except ValidationException as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    gen_pki()
