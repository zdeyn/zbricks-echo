# tests/machines/test_request_response.py
import pytest
from rich import print

from zbricks.machines.request_response import zRequestResponseMachine, Request, Response
from zbricks.machines.request_response import zUnknownMethodException
from zbricks.machines.request_response import logger
logger.setLevel('DEBUG')

from ..helpers import create_request


def test_returns_request(machine : zRequestResponseMachine):
            
    request : Request = create_request('GET', '/test')
    response : Response = machine.handle_request(request)

    assert isinstance(request, Request)


def test_defaults_to_text_plain_utf8(machine : zRequestResponseMachine):
            
    request : Request = create_request('GET', '/test')
    response : Response = machine.handle_request(request)

    assert response.content_type == 'text/plain; charset=utf-8'


def test_500_internal_server_error(machine : zRequestResponseMachine):
    
    request : Request = create_request('FOO', '/forcing-an-error')
    response : Response = machine.handle_request(request)
    
    assert response.status_code == 500
    raw_data : bytes = response.data
    data = raw_data.decode()
    print('\n', data)
    assert data.startswith('Internal Server Error:')


def test_can_define_route(machine : zRequestResponseMachine):

    @machine.route('/foo')
    def foo_handler(request : Request) -> Response:
        return Response('Foo Response')
        
    request : Request = create_request('GET', '/foo')
    response : Response = machine.handle_request(request)
    
    assert response.status_code == 200
    assert response.data == b'Foo Response'



def test_default_404_not_found(machine : zRequestResponseMachine):
    
    request : Request = create_request('GET', '/default-does-not-exist')
    response : Response = machine.handle_request(request)
    
    assert response.status_code == 404
    assert response.data == b'Default 404 Error: /default-does-not-exist'



def test_custom_404_not_found(machine : zRequestResponseMachine):

    @machine.error(404)
    def four_oh_four(request : Request) -> Response:
        return Response(f'Custom Four Oh Four Error: {request.path}', status=404)
    
    request : Request = create_request('GET', '/custom-does-not-exist')
    response : Response = machine.handle_request(request)
    
    assert response.status_code == 404
    assert response.data == b'Custom Four Oh Four Error: /custom-does-not-exist'