# tests/test_auth_routes.py
from typing import Any, Callable, Generator, Iterable, Tuple, Union
import pytest

from unittest.mock import MagicMock
from flask import Flask, make_response
from rich import print
# from flask.testing import FlaskClient
from pytest_mock import MockFixture

from zbricks.base import zBrick, zCallableAugmentation, handler
from zbricks.bricks import zWsgiApplication
from werkzeug.wrappers import Request, Response
from werkzeug.test import Client
    

class Test_zBrick:

    def test_can_exist(self):
        """A zBrick can exist."""
        brick = zBrick()

    def test_is_boring(self):
        """A zBrick is boring by default, but instantiable."""
        brick = zBrick()

        # has no call handler
        with pytest.raises(NotImplementedError) as e:
            brick()
        assert e.match("ot intended for use as a callable")

        # has no iterator handler
        with pytest.raises(NotImplementedError) as e:
            i = iter(brick)
        assert e.match("ot intended for use as an iterator")

        # has no generator handler
        with pytest.raises(NotImplementedError) as e:
            g = next(brick)
        assert e.match("ot intended for use as a generator")

        # has no context management entry handler
        with pytest.raises(NotImplementedError) as e:
            with brick:
                pass
        assert e.match("ot intended for use as a context manager")
        assert e.match("enter")

        # has no context management exit handler
        class HalfCM(zBrick):
            def __enter__(self): pass
        half_cm = HalfCM()    
        with pytest.raises(NotImplementedError) as e:
            with half_cm:
                pass
        assert e.match("ot intended for use as a context manager")
        assert e.match("exit")

class Test_zBrick_Augmentation:

    def test_decorator_exists(self):
        """The `handler` decorator exists."""
        assert callable(handler)
        pass


class Test_zCallableAugmentation:    

    def test_exception_no_handlers_registered(self):
        """A zBrick raises an exception when called if no handlers are registered."""

        brick = zBrick()
        with pytest.raises(NotImplementedError) as e:
            brick()

        assert e.match("ot intended for use as a callable")
    
    def test_handler_is_called_when_expected(self):
        """A zBrick calls the handler which matches the signature"""

        class TestBrick(zCallableAugmentation, zBrick):
            _handler_counter = 0
            _handler_log = []

            @handler('call', sig=str)
            def _handler(self, my_string: str) -> Any:
                self._handler_counter += 1
                self._handler_log.append(my_string)

        brick = TestBrick()
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
        class GreeterBrick(zCallableAugmentation, zBrick):

            @handler('call', sig=str)
            def _handler(self, target: str) -> Any:
                return f"Hello, {target}!"

            @handler('call', sig=list)
            def _list_handler(self, targets: list) -> Any:
                return '\n'.join(f"Hello, {target}!" for target in targets)

        brick = GreeterBrick()
        assert brick('LiLi') == ["Hello, LiLi!"]
        assert brick(['Gary', 'Varian']) == ["Hello, Gary!\nHello, Varian!"]

        with pytest.raises(NotImplementedError) as e:
            brick(1)

        assert e.match("o handlers registered for __call__ input (int): |1|")
    
    def test_match_compound_input(self):
        """A zBrick decomposes and matches compound input."""
        class FakeWsgiBrick(zCallableAugmentation, zBrick):
            @handler('call', sig=(dict, Callable))
            def _handler(self, environ: dict, start_response: Callable):
                assert isinstance(environ, dict)
                assert callable(start_response)
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return 'Hello, World!'

        brick = FakeWsgiBrick()
        client = Client(brick)
        response = client.get('/')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'