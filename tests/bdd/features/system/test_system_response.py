import pytest
from rich import print
from pytest_bdd import scenarios, scenario, given, when, then
from flask.testing import FlaskClient

from zbricks import zApp, Response

scenarios("system")

# --=[ Givens: Systems ]=--
# remember, givens need @pytest.fixture decorator

@pytest.fixture
@given('a system', target_fixture="system")
def system():
    zapp = zApp(__name__)
    return zapp

@pytest.fixture
@given('a system with a resource', target_fixture="system")
def system_with_resource(system:zApp):
    @system.route("/resource")
    def hello():
        return "Hello, World!"
    return system

@pytest.fixture
@given('a system with a bugged resource', target_fixture="system")
def system_with_bugged_resource(system:zApp):
    @system.route("/resource")
    def hello():
        raise Exception("This is a bug")
    return system

# --=[ Givens: Clients ]=--

@given('a client', target_fixture="client")
def client(system: zApp):
    with system.test_client() as client:
        return client

# --=[ Whens ]=--

@when('a request is made for a non-existent resource', target_fixture="response")
def client_makes_a_request(client: FlaskClient) -> Response:
    return client.get('/not-a-resource')

@when('the client makes a request', target_fixture="response")
@when('a request is made for that resource', target_fixture="response")
def client_makes_a_request_for_resource(client: FlaskClient) -> Response:
    return client.get('/resource')

# --=[ Thens ]=--

@then('the system responds with a Response object')
def it_responds_to_requests(response: Response) -> bool:
    return isinstance(response, Response)

@then('the system responds with 200 OK')
def it_responds_with_200(response: Response) -> bool:
    return response.status_code == 200

@then('the system responds with 404 Not Found')
def it_responds_with_404(response: Response) -> bool:
    return response.status_code == 404

@then('the system responds with 500 Internal Server Error')
def it_responds_with_404(response: Response) -> bool:
    return response.status_code == 500
