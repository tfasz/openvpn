# pylint: disable=import-error,invalid-name,missing-function-docstring,missing-module-docstring,wrong-import-position
import os
import os.path
import shutil
import sys

from datetime import datetime

PKI_BIN_DIR = "/usr/share/easy-rsa"

test_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_dir, "../ovpn"))
from ovpn_util import read_file

sample_dir = os.path.join(test_dir, "sample-input")
temp_dir = os.path.join(test_dir, "temp")

# Some tests generate a new PKI in the temp dir on each run.
temp_pki_dir = os.path.join(test_dir, "temp/pki")

def get_expected_output_file(file_name):
    expected_output_dir = os.path.join(test_dir, "expected-output")
    return os.path.join(expected_output_dir, file_name)

def read_expected_output(file_name):
    return read_file(get_expected_output_file(file_name))

def rm_tree(delete_dir):
    if os.path.exists(delete_dir):
        shutil.rmtree(delete_dir)

def day_diff_now(date):
    return day_diff(date, datetime.now())

def day_diff(date1, date2):
    diff = date1 - date2
    return diff.days

def assert_between(value, low, high):
    assert value >= low
    assert value <= high
