# tests/steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from werkzeug.test import Client
from werkzeug.wrappers import Response
from zbricks import zApp
from flask import Flask

@pytest.fixture
def app():
    return zApp()
    # return Flask(__name__)

@pytest.fixture
def client(app):
    return Client(app, Response)

@given(parsers.parse('the endpoint "{endpoint}" exists'))
def app_with_endpoint(app, endpoint):
    @app.route(endpoint)
    def hello():
        return Response('Hello, World!', status=200, content_type='text/plain')

@given(parsers.parse('the endpoint "{endpoint}" returns "{response_text}"'))
def app_with_endpoint_returns(app, endpoint, response_text):
    @app.route(endpoint)
    def hello_with_given_text():
        return Response(f'{response_text}', status=200, content_type='text/plain')

@when(parsers.parse('I request the "{endpoint}" endpoint'))
def request_endpoint(client, endpoint):
    client.request = client.get(endpoint)

@then(parsers.parse('I should get a "{status_code:d}" status code'))
def check_status_code(client, status_code):
    assert client.request.status_code == status_code

@then(parsers.parse('I should see "{response_text}"'))
def check_response_text(client, response_text):
    actual = client.request.data.decode()
    assert response_text in actual
