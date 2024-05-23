import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from typing import Generator

from zbricks import zApp, Request, Response

@pytest.fixture
def app() -> Generator[zApp, None, None]:

    zapp = zApp(__name__)
   
    yield zapp

@pytest.fixture
def client(app : zApp) -> Generator[Request, None, None]:
    with app.test_client() as client:
        yield client