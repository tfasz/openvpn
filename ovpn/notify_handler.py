#!/usr/bin/env python3
# pylint: disable=too-many-function-args
"""
Handle notifications on VPN connect and disconnect events.
"""

from ovpn_util import load_config
from slack_sdk.webhook import WebhookClient

class NotificationHandler:
    """Manage notifications"""
    def __init__(self, vpn_dir, event_type, connect_time, duration, client_ip, client_name, bytes_sent, bytes_received):
        """Notify subscribers on client connect and disconnect events."""
        self.msg = None
        # Based on config set our notification processor
        config = load_config(vpn_dir)
        if "slack_notify_url" in config:
            self.handler = SlackNotification(config["slack_notify_url"])

        # Based on event type setup message details
        if event_type == "client-connect":
            self.msg = f"User {client_name} connected @ {connect_time} from {client_ip}"
        elif event_type == "client-disconnect":
            dur = get_duration_text(duration)
            self.msg = f"User {client_name} disconnected after {dur}, sent: {bytes_sent:,.0f}, received: {bytes_received:,.0f}"

    def set_handler(self, handler):
        """Override default notification hanlder (currently used for testing)"""
        self.handler = handler

    def send(self):
        """Sent our message to the relevant handler"""
        if self.handler and self.msg:
            return self.handler.send(self.msg)
        return None

class SlackNotification:
    """Send a webhook to Slack"""
    def __init__(self, url):
        """Init our client"""
        self.url = url

    def send(self, msg):
        """Send our notification"""
        client = WebhookClient(self.url)
        response = client.send(text=msg)
        print(f"Slack notification status #{response.status_code}:{response.body}")
        return response

def get_duration_text(duration):
    """Get a friendly text string for the connected duration"""
    if duration < (60 * 2):
        return str(duration) + "s"
    if duration < (60 * 60 * 2):
        return str(round(duration/60)) + "m"
    return str(round(duration/3600)) + "h"
