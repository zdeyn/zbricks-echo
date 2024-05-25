# tests/test_basics.py
import pytest
from rich import print

from zbricks import zApp, Flask, Request, Response

# @pytest.mark.skip
def test_responds(system : zApp) -> None:
            
    with system.test_client() as client:
        response = client.get('/')
        assert isinstance(response, Response)
        