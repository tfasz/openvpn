#!/usr/bin/env python3
# pylint: disable=no-value-for-parameter,unused-argument
"""
Trigger notifications on connect and disconnect events. This is called directly via the client-connect
and client-disconnect script reference in the server.conf file. Values are passed as env vars by the OpenVPN
process - see examples below.
"""

import click
from notify_handler import NotificationHandler

@click.command()
@click.argument("file", required=False)
@click.option("-D", "--vpndir", default='/etc/openvpn', help="OpenVPN config directory")
@click.option("-e", "--event-type", envvar='script_type', help="Event type - connect, disconnect, etc.", metavar="<EVENT_TYPE>")
@click.option("-t", "--connect-time", envvar='time_ascii', help="Connection time", metavar="<TIME>")
@click.option("-d", "--duration", type=int, envvar='time_duration', help="Duration of connection", metavar="<SECONDS>")
@click.option("-i", "--client-ip", envvar='trusted_ip', help="Connection IP", metavar="<IP>")
@click.option("-c", "--client-name", envvar='common_name', help="Client common name", metavar="<NAME>")
@click.option("-s", "--sent", type=int, envvar='bytes_sent', help="Bytes sent", metavar="<NUM>")
@click.option("-r", "--received", type=int, envvar='bytes_received', help="Bytes received", metavar="<NUM>")
def notify(vpndir, event_type, connect_time, duration, client_ip, client_name, sent, received, file=None):
    """Trigger notification handler on client connect and disconnect events."""
    handler = NotificationHandler(vpndir, event_type, connect_time, duration, client_ip, client_name, sent, received)
    handler.send()

if __name__ == '__main__':
    notify()

# Example vars on connect:
# environ({
#   'client_connect_deferred_file': '/tmp/openvpn_ccr_429836424518bf837a53989d3a2c9b82.tmp',
#   'client_connect_config_file': '/tmp/openvpn_cc_52e7c630cdae4aa3a8fef36de7f3204.tmp',
#   'script_type': 'client-connect',
#   'time_unix': '1652361695',
#   'time_ascii': '2022-05-12 13:21:35',
#   'ifconfig_pool_netmask': '255.255.255.0',
#   'ifconfig_pool_remote_ip': '192.168.255.2',
#   'trusted_port': '14470',
#   'trusted_ip': '207.180.135.101',
#   'common_name': '<USERNAME>',
#   'IV_BS64DL': '1',
#   'IV_SSO': 'webauth,openurl',
#   'IV_GUI_VER': 'net.openvpn.connect.android_3.2.7-7957',
#   'IV_AUTO_SESS': '1',
#   'IV_IPv6': '0',
#   'IV_CIPHERS': 'AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:BF-CBC',
#   'IV_PROTO': '30',
#   'IV_TCPNL': '1',
#   'IV_NCP': '2',
#   'IV_PLAT': 'android',
#   'IV_VER': '3.git::d3f8b18b:Release',
#   'untrusted_port': '14470',
#   'untrusted_ip': '207.180.135.101',
#   'tls_serial_hex_0': 'cf:c9:3f:d8:1a:1f:...',
#   'tls_serial_0': '2761951417092...',
#   'tls_digest_sha256_0': '69:96:4f:e1:d2:...',
#   'tls_digest_0': 'c2:d3:58:f7:42:...',
#   'tls_id_0':
#   'CN=<USERNAME>',
#   'X509_0_CN': '<USERNAME>',
#   'tls_serial_hex_1': '39:1e:7e:03:e8:...',
#   'tls_serial_1': '3260924...',
#   'tls_digest_sha256_1': '40:9f:68:3f:0f:...',
#   'tls_digest_1': 'ac:5c:72:63:...',
#   'tls_id_1': 'CN=vpn.example.com',
#   'X509_1_CN': 'vpn.example.com',
#   'remote_port_1': '1194',
#   'local_port_1': '1194',
#   'proto_1': 'tcp4-server',
#   'daemon_pid': '1',
#   'daemon_start_time': '1652064617',
#   'daemon_log_redirect': '0',
#   'daemon': '0',
#   'verb': '3',
#   'config': '/etc/openvpn/server.conf',
#   'ifconfig_local': '192.168.255.1',
#   'ifconfig_netmask': '255.255.255.0',
#   'route_net_gateway': '172.25.0.1',
#   'route_vpn_gateway': '192.168.255.2',
#   'route_network_1': '192.168.254.0',
#   'route_netmask_1': '255.255.255.0',
#   'route_gateway_1': '192.168.255.2',
#   'script_context': 'init',
#   'tun_mtu': '1500',
#   'link_mtu': '1623',
#   'dev': 'tun0',
#   'dev_type': 'tun',
#   'redirect_gateway': '0'})
#
# Example vars on disconnect:
# environ({
#   'script_type': 'client-disconnect',
#   'time_duration': '4',
#   'bytes_sent': '2915',
#   'bytes_received': '3498',
#   'trusted_port': '14470',
#   'trusted_ip': '207.180.135.101',
#   'ifconfig_pool_netmask': '255.255.255.0',
#   'ifconfig_pool_remote_ip': '192.168.255.2',
#   'time_unix': '1652361695',
#   'time_ascii': '2022-05-12 13:21:35',
#   'common_name': '<USERNAME>',
#   'IV_BS64DL': '1',
#   'IV_SSO': 'webauth,openurl',
#   'IV_GUI_VER': 'net.openvpn.connect.android_3.2.7-7957',
#   'IV_AUTO_SESS': '1',
#   'IV_IPv6': '0',
#   'IV_CIPHERS': 'AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:BF-CBC',
#   'IV_PROTO': '30',
#   'IV_TCPNL': '1',
#   'IV_NCP': '2',
#   'IV_PLAT': 'android',
#   'IV_VER': '3.git::d3f8b18b:Release',
#   'untrusted_port': '14470',
#   'untrusted_ip': '207.180.135.101',
#   'tls_serial_hex_0': 'cf:c9:3f:d8:...',
#   'tls_serial_0': '2761951....',
#   'tls_digest_sha256_0': '69:96:4f:e1:d2:...',
#   'tls_digest_0': 'c2:d3:58:f7:42:...',
#   'tls_id_0': 'CN=<USERNAME>',
#   'X509_0_CN': '<USERNAME>',
#   'tls_serial_hex_1': '39:1e:7e:03:e8:9f:...',
#   'tls_serial_1': '326092473...',
#   'tls_digest_sha256_1': '40:9f:68:3f:0f:...',
#   'tls_digest_1': 'ac:5c:72:63:...',
#   'tls_id_1': 'CN=vpn.example.com',
#   'X509_1_CN': 'vpn.example.com',
#   'remote_port_1': '1194',
#   'local_port_1': '1194',
#   'proto_1': 'tcp4-server',
#   'daemon_pid': '1',
#   'daemon_start_time': '1652064617',
#   'daemon_log_redirect': '0',
#   'daemon': '0',
#   'verb': '3',
#   'config': '/etc/openvpn/server.conf',
#   'ifconfig_local': '192.168.255.1',
#   'ifconfig_netmask': '255.255.255.0',
#   'route_net_gateway': '172.25.0.1',
#   'route_vpn_gateway': '192.168.255.2',
#   'route_network_1': '192.168.254.0',
#   'route_netmask_1': '255.255.255.0',
#   'route_gateway_1': '192.168.255.2',
#   'script_context': 'init',
#   'tun_mtu': '1500',
#   'link_mtu': '1623',
#   'dev': 'tun0',
#   'dev_type': 'tun',
#   'redirect_gateway': '0'})
