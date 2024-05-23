# test_system_response.py
import pytest
from pytest_bdd import scenarios, given, when, then
from flask.testing import FlaskClient

from tests.conftest import app, client

from zbricks import zApp, Request, Response

# This line will include the feature file in the test suite
scenarios('features/system-responds.feature')

@given('there is a system')
def system(app : zApp) -> zApp:
    return app

@then('it responds to requests')
def it_responds_to_requests(client: FlaskClient) -> bool:
    response = client.get('/')
    assert isinstance(response, Response)