#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter
"""CLI to revoke the ovpn cert for a user."""
import sys
import click
from client_config import ClientConfig
from ovpn_util import ValidationException

@click.command()
@click.argument("name")
@click.option("-D", "--vpndir", envvar='OPENVPN', help="OpenVPN config directory")
@click.option("-b", "--bindir", envvar='EASYRSA', help="PKI binary directory")
def revoke_client(name, vpndir, bindir):
    """Revoke the ovpn cert file for a user."""
    try:
        client_config = ClientConfig(vpndir, bindir)
        client_config.revoke(name)
    except ValidationException as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    revoke_client()
