# tests/steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from flask.testing import FlaskClient
from werkzeug.wrappers import Request, Response
from zbricks import zApp, zEventDispatcher
from flask import Flask

@pytest.fixture
def storage(app : zApp) -> dict:
    return {'app': app, 'response': None}

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

@given('the event dispatcher is installed')
def install_event_dispatcher(app : zApp):
    # zevent = zEventDispatcher(app)
    pass # installed by default

@when(parsers.parse('I request the "{endpoint}" endpoint'))
def request_endpoint(client : FlaskClient, endpoint, storage):
    storage['response'] = client.get(endpoint)

@then(parsers.parse('I should get a "{status_code:d}" status code'))
def check_status_code(status_code, storage):
    # print(storage['response'].data.decode(), storage['response'].status_code)
    assert storage['response'].status_code == status_code

@then(parsers.parse('I should see "{response_text}"'))
def check_response_text(client : FlaskClient, response_text, storage):
    actual = storage['response'].data.decode()
    assert response_text in actual

@when('the event dispatcher receives the request')
def event_dispatcher_receives_request(client : FlaskClient, storage):
    with storage['app'].test_request_context('/handled-by-event'):
        storage['response'] = client.get('/handled-by-event')

@then('the event dispatcher is called')
def check_event_dispatcher_called(storage):
    # Check that the dispatcher handled the request
    assert storage['response'].status_code == 200
    assert storage['response'].data.decode() == "Handled by event dispatcher"

@when('the event dispatcher finds no handlers for the request')
def event_dispatcher_no_handler(client : FlaskClient, storage):
    with storage['app'].test_request_context('/non-existent'):
        storage['response'] = client.get('/non-existent')

@then('Flask handles the 404 error')
def check_flask_handles_404(storage):
    # Check that Flask handled the 404 error
    assert storage['response'].status_code == 404
    assert "Not Found" in storage['response'].data.decode()