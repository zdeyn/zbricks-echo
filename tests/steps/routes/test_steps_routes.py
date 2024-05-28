import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pytest_bdd.exceptions import NoScenariosFound

from flask.testing import FlaskClient
from werkzeug.wrappers import Response
from zbricks import zApp

try:
    scenarios('features/routes/')
except NoScenariosFound:
    pass

@given(parsers.parse('the endpoint "{endpoint}" exists'))
def app_with_endpoint(app : zApp, endpoint):
    @app.route(endpoint)
    def hello():
        return Response('Hello, World!', status=200, content_type='text/plain')


@given(parsers.parse('the endpoint "{endpoint}" returns "{response_text}"'))
def app_with_endpoint_returns(app : zApp, endpoint, response_text):
    @app.route(endpoint)
    def hello_with_given_text():
        return Response(f'{response_text}', status=200, content_type='text/plain')


@when(parsers.parse('I request the "{endpoint}" endpoint'))
def request_endpoint(client : FlaskClient, endpoint, storage):
    storage['response'] = client.get(endpoint)


@then(parsers.parse('I should get a "{status_code:d}" status code'))
def check_status_code(status_code, storage):
    assert storage['response'].status_code == status_code


@then(parsers.parse('I should see "{response_text}"'))
def check_response_text(client : FlaskClient, response_text, storage):
    # print(storage['response'])
    actual = storage['response'].data.decode()
    assert response_text in actual