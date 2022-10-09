"""Location for pytest fixtures."""
import os
import pytest
from tests import test_dir, temp_dir, rm_tree

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Run cleanup logic at end of all tests"""
    def clear_temp():
        """"Clear temp directory"""
        rm_tree(temp_dir)

    def remove_crl():
        """"Clear CRL from test directory as it changes every time we run"""
        os.remove(os.path.join(test_dir, "crl.pem"))

    request.addfinalizer(clear_temp)
    request.addfinalizer(remove_crl)
