# pylint: disable=import-error,invalid-name,missing-function-docstring,missing-module-docstring,wrong-import-position
import os.path
import shutil
import sys

PKI_BIN_DIR = "/usr/share/easy-rsa"

test_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_dir, "../ovpn"))
from ovpn_util import read_file

temp_dir = os.path.join(test_dir, "temp")
# Some tests use a static PKI bin directory which is checked into git
static_pki_dir = os.path.join(test_dir, "test-pki")
# Some tests generate a new PKI in the temp dir on each run.
temp_pki_dir = os.path.join(test_dir, "temp/pki")

def get_expected_output_file(file_name):
    expected_output_dir = os.path.join(test_dir, "expected-output")
    return os.path.join(expected_output_dir, file_name)

def read_expected_output(file_name):
    return read_file(get_expected_output_file(file_name))

def read_temp_file(file_name):
    return read_file(os.path.join(temp_dir, file_name))

def rm_tree(delete_dir):
    if os.path.exists(delete_dir):
        shutil.rmtree(delete_dir)
