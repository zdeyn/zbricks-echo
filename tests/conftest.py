import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from typing import Generator

from .helpers import create_request as _create_request

from zbricks import zApp, Request, Response

@pytest.fixture
def app() -> Generator[zApp, None, None]:

    zapp = zApp(__name__)
   
    yield zapp
