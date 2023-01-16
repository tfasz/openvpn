#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter
"""CLI to output the ovpn config file for a user."""
import sys
import click
from client_config import ClientConfig
from ovpn_util import render_template, ValidationException

@click.command()
@click.argument("name")
@click.option("-D", "--vpndir", envvar='OPENVPN', help="OpenVPN config directory")
@click.option("-b", "--bindir", envvar='EASYRSA', help="PKI binary directory")
def get_client(name, vpndir, bindir):
    """Get the ovpn config file for a user."""
    try:
        client_config = ClientConfig(vpndir, bindir)
        print(render_template("client.ovpn.j2", client_config.get(name)))
    except ValidationException as ex:
        print(ex)
        sys.exit(1)

if __name__ == '__main__':
    get_client()
