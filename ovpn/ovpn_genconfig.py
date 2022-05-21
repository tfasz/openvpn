#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter
"""CLI to generate the VPN server config file from args."""
import click
from server_config import ServerConfig

@click.command()
@click.argument("name")
@click.option("-p", "--port", type=int, default=1194, help="Network port VPN will listen for traffic", metavar="<PORT>")
@click.option("-t", "--tcp", is_flag=True, help="Enable TCP instead of UDP protocol")
@click.option("-d", "--dns", multiple=True, help="Add dns server to the list", metavar="<IP>")
@click.option("-D", "--vpndir", envvar='OPENVPN', help="OpenVPN config directory", metavar="<DIR>")
@click.option("-s", "--slack-notify", help="Slack webhook URL to notify on connect/disconnect events", metavar="<URL>")
def gen_server(vpndir, name, port, tcp, dns, slack_notify):
    """Generate VPN server config for NAME"""
    server_config = ServerConfig(vpndir, name, port, tcp, dns, slack_notify)
    server_config.save()

if __name__ == '__main__':
    gen_server()
