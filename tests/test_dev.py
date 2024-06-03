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

class Test_zBrick:

    def test_cannot_instantiate_abstract(self):
        """A zBrick is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            zBrick()
    
    def test_can_instantiate_once_handler_is_defined(self):
        """A zBrick can be instantiated once the _handler method is defined."""
        class ConcreteBrick(zBrick):
            def _handler(self): pass

        brick = ConcreteBrick()
        assert brick is not None # brick exists

class Test_zBrick_As_Callable:    

    def test_exception_no_handlers_registered(self):
        """A zBrick raises an exception when called if no handlers are registered."""
        class ConcreteBrick(zBrick):
            def _handler(self): pass

        brick = ConcreteBrick()
        with pytest.raises(NotImplementedError) as e:
            brick()

        assert e.match("ot intended for use as a callable")
    
    def test_handler_is_called_when_expected(self):
        """A zBrick calls the handler which matches the signature"""
        class CountingLoggerBrick(zBrick):
            _handler_counter = 0
            _handler_log = []

            @call_handler(str)
            def _handler(self, my_string: str) -> Any:
                self._handler_counter += 1
                self._handler_log.append(my_string)

        brick = CountingLoggerBrick()
        assert brick._handler_counter == 0
        assert brick._handler_log == []

        brick('foo')
        assert brick._handler_counter == 1
        assert brick._handler_log == ['foo']

        brick('bar')
        assert brick._handler_counter == 2
        assert brick._handler_log == ['foo', 'bar']
    
    def test_exception_no_handlers_matched(self):
        """A zBrick raises an exception when called if no handlers match the signature."""
        class GreeterBrick(zBrick):

            @call_handler(str)
            def _handler(self, target: str) -> Any:
                return f"Hello, {target}!"

            @call_handler(list)
            def _list_handler(self, targets: list) -> Any:
                return '\n'.join(f"Hello, {target}!" for target in targets)

        brick = GreeterBrick()
        assert brick('LiLi') == "Hello, LiLi!"
        assert brick(['Gary', 'Varian']) == "Hello, Gary!\nHello, Varian!"

        with pytest.raises(NotImplementedError) as e:
            brick(1)

        assert e.match("o handlers registered for __call__ input (int): |1|")
    
    def test_match_compound_input(self):
        """A zBrick decomposes and matches compound input."""
        class FakeWsgiBrick(zBrick):
            @call_handler(dict, Callable)
            def _handler(self, environ: dict, start_response: Callable):
                assert isinstance(environ, dict)
                assert callable(start_response)
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return ['Hello, World!']

        brick = FakeWsgiBrick()
        client = Client(brick)
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'
    
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
        