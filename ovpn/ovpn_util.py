"""Utility functions used across our various scripts."""
import json
import os.path
import subprocess
from jinja2 import Environment, FileSystemLoader

class ValidationException(Exception):
    """Exception used when validation issues occur."""

def get_vpn_config_file(vpn_dir, config_file_name):
    """Get the file name for our VPN config file"""
    return os.path.join(vpn_dir, config_file_name)

def config_exists(vpn_dir, config_file_name="config.json"):
    """Check if our VPN config file exists"""
    return os.path.exists(os.path.join(vpn_dir, config_file_name))

def load_config(vpn_dir, config_file_name="config.json"):
    """Load the contents of the VPN config and return as dictionary"""
    if not config_exists(vpn_dir, config_file_name):
        raise ValidationException("No config file exists - have you run ovpn_genconfig?")
    config_file = get_vpn_config_file(vpn_dir, config_file_name)
    return load_json(config_file)

def load_json(json_file):
    """Load a JSON file and return as dictionary"""
    with open(json_file, "r", encoding="utf8") as file:
        return json.load(file)

def read_file(file_path):
    """Read the contents of a file into a string"""
    with open(file_path, 'r', encoding="utf8") as file:
        return file.read()

def read_x509(file_path):
    """Read the X509 certificate value from a file using OpenSSL"""
    result = subprocess.run(["openssl", "x509", "-in", file_path], capture_output=True, check=True)
    return result.stdout.decode()

def render_template(template_file, template_data):
    """Render a template from the provided template file name and data"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader = FileSystemLoader(template_dir), autoescape = True)
    template = env.get_template(template_file)
    return template.render(template_data)

def save_config(data, vpn_dir, config_file_name="config.json"):
    """Save our config file"""
    config_file = get_vpn_config_file(vpn_dir, config_file_name)
    write_json(config_file, data)

def write_file(file_path, contents):
    """Write the contents of a string to specified file name"""
    with open(file_path, "w", encoding="utf8") as file:
        file.write(contents)

def write_json(file_path, data):
    """Write the contents of a dict to specified file name"""
    with open(file_path, "w", encoding="utf8") as file:
        json.dump(data, file, indent=2)
