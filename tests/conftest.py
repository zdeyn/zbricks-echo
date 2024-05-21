import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from typing import Generator

from .helpers import create_request as _create_request

from zbricks.machines.request_response import zRequestResponseMachine, Request, Response

@pytest.fixture
def machine() -> Generator[zRequestResponseMachine, None, None]:

    m = zRequestResponseMachine()
   
    yield m
