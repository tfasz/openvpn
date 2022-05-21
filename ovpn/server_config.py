"""Generate the VPN server config file from arguments passed in"""
import os
from ovpn_util import render_template, save_config, write_file

class ServerConfig:
    """Track server config values and generate config file"""
    def __init__(self, vpn_dir, name, port, tcp, dns_servers, slack_notify_url=None):
        self.vpn_dir = vpn_dir
        self.data = {}
        self.data['common_name'] = name
        self.data['port'] = port
        self.data['proto'] = "tcp4" if tcp else "udp4"
        self.data['dns_servers'] = dns_servers
        self.data['slack_notify_url'] = slack_notify_url

    def render(self):
        """Get the server config as a string"""
        return render_template("server.conf.j2", self.data)

    def save(self):
        """Save the server config to server.conf"""
        # save in JSON format for later use
        save_config(self.data, self.vpn_dir)
        # and write our VPN conf file
        write_file(os.path.join(self.vpn_dir, "server.conf"), self.render())
