import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pytest_bdd.exceptions import NoScenariosFound

from flask.testing import FlaskClient
from werkzeug.wrappers import Response
from zbricks import zApp

try:
    scenarios('features/auth/')
except NoScenariosFound:
    pass


@when(parsers.parse('I request the "{endpoint}" endpoint'))
def request_endpoint(client : FlaskClient, endpoint, storage):
    storage['response'] = client.get(endpoint)

@then(parsers.parse('I should get a "{status_code:d}" status code'))
def check_status_code(status_code, storage):
    # print(storage['response'].data.decode(), storage['response'].status_code)
    assert storage['response'].status_code == status_code

@then(parsers.parse('I should see "{response_text}"'))
def check_response_text(response_text, storage):
    actual = storage['response'].data.decode()
    assert response_text in actual

@then(parsers.parse('I should see "{header_value}" in the "{header_field}" field of the response headers'))
def check_response_headers(header_value, header_field, storage):
    actual = storage['response'].headers[header_field]
    assert header_value in actual