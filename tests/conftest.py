import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from typing import Generator

from pytest_bdd import scenarios, scenario, given, when, then

from zbricks import zApp, Request, Response

@pytest.fixture
@given('a system', target_fixture="system")
def system():
    zapp = zApp(__name__)
    return zapp

# --=[ Givens: Clients ]=--

@given('a client', target_fixture="client")
def client(system: zApp):
    with system.test_client() as client:
        return client