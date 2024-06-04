# tests/test_auth_routes.py
from typing import Any, Callable, Iterable, Tuple, Union
import pytest

from unittest.mock import MagicMock
from flask import Flask, make_response
from rich import print
# from flask.testing import FlaskClient
from pytest_mock import MockFixture

from zbricks.base import zBrick, call_handler
from zbricks.bricks import zWsgiApplication
from werkzeug.wrappers import Request, Response
from werkzeug.test import Client
    
class Test_zWsgiApplication_Dev:
    
    @pytest.mark.skip(reason="Fix once zCallableAugmentation is completed")
    def test_404(self):        
        brick = zWsgiApplication(name = 'wsgi')
        assert brick is not None
        client = Client(brick)
        response = client.get('/not-there')
        assert response.status_code == 404
        assert response.data == b'404 Not Found: /not-there'
    
    @pytest.mark.skip(reason="Fix once zCallableAugmentation is completed")
    def test_200(self):        
        brick = zWsgiApplication(name = 'wsgi')

        @brick.route('/hello')
        def index(request: Request):
            # see if name= is in the query string
            name = request.args.get('name', 'World')
            return Response(f'Hello, {name}!')
        
        assert brick is not None
        client = Client(brick)
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'

        query_response = client.get('/hello?name=foo')
        assert query_response.status_code == 200
        assert query_response.data == b'Hello, foo!'
        