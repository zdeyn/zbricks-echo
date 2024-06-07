# tests/test_auth_routes.py
from typing import Any, Callable, Generator, Iterable, Tuple, Union
import pytest

from unittest.mock import MagicMock
from rich import print
from pytest_mock import MockFixture
from werkzeug import Client

from zbricks import zBrick, handler
from zbricks.studs import zDataStorageStud
from zbricks.augmentations import zAugmentationEntry

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

class Test_zAugmentation:

    def test_decorator_exists(self):
        """The `handler` decorator exists."""
        assert callable(handler)

    def test_decorator_registers_function(self):
        """The `handler` decorator registers a function correctly."""
        class TestBrick(zBrick):
            @handler('test_aug')
            def test_method(self):
                pass

        brick = TestBrick()
        storage : zDataStorageStud[zAugmentationEntry] = getattr(brick, '_aug_data')
        assert isinstance(storage, zDataStorageStud)
        
        # Check that the registry has an entry for the decorated method
        assert len(storage._data) == 1
        assert storage._data[0].method.__name__ == 'test_method'
        assert storage._data[0].aug == 'test_aug'

    def test_multiple_decorators(self):
        """The `handler` decorator registers multiple functions correctly."""
        class TestBrick(zBrick):
            @handler('aug1')
            def method_one(self):
                pass
            
            @handler('aug2')
            def method_two(self):
                pass

        brick = TestBrick()
        storage : zDataStorageStud[zAugmentationEntry] = getattr(brick, '_aug_data')
        assert isinstance(storage, zDataStorageStud)

        # Check that the registry has entries for both decorated methods
        assert len(storage._data) == 2
        methods = {entry.method.__name__: entry.aug for entry in storage._data}
        assert methods == {'method_one': 'aug1', 'method_two': 'aug2'}

    def test_decorator_with_args(self):
        """The `handler` decorator registers a function with arguments correctly."""
        class TestBrick(zBrick):
            @handler('test_aug', 'arg1', kwarg1='value1')
            def test_method(self, arg1, kwarg1):
                pass

        brick = TestBrick()
        storage : zDataStorageStud[zAugmentationEntry] = getattr(brick, '_aug_data')
        assert isinstance(storage, zDataStorageStud)
        
        # Check that the registry has an entry with the correct args and kwargs
        assert len(storage._data) == 1
        entry : zAugmentationEntry = storage._data[0]
        assert entry.method.__name__ == 'test_method'
        assert entry.aug == 'test_aug'
        assert entry.args == ('arg1',)
        assert entry.kwargs == {'kwarg1': 'value1'}

    def test_decorator_on_inherited_method(self):
        """The `handler` decorator works with inherited methods."""
        class BaseBrick(zBrick):
            @handler('base_aug')
            def base_method(self):
                pass

        class InheritedBrick(BaseBrick):
            @handler('inherited_aug')
            def inherited_method(self):
                pass

        brick = InheritedBrick()
        storage : zDataStorageStud[zAugmentationEntry] = getattr(brick, '_aug_data')
        assert isinstance(storage, zDataStorageStud)

        # Check that the registry has entries for both base and inherited methods
        assert len(storage._data) == 2
        methods = {entry.method.__name__: entry.aug for entry in storage}
        assert methods == {'base_method': 'base_aug', 'inherited_method': 'inherited_aug'}

    def test_conflicting_decorator_names(self):
        """The `handler` decorator handles conflicting names gracefully."""
        class TestBrick(zBrick):
            @handler('conflict_aug')
            def method_one(self):
                pass

            @handler('conflict_aug')
            def method_two(self):
                pass

        brick = TestBrick()
        storage : zDataStorageStud[zAugmentationEntry] = getattr(brick, '_aug_data')
        assert isinstance(storage, zDataStorageStud)

        # Check that the registry has entries for both methods even with the same aug name
        assert len(storage._data) == 2
        assert storage._data[0].method.__name__ == 'method_one'
        assert storage._data[0].aug == 'conflict_aug'
        assert storage._data[1].method.__name__ == 'method_two'
        assert storage._data[1].aug == 'conflict_aug'



class Test_zCallHandlerAugmentation:

    def test_exception_no_handlers_registered(self):
        """A zBrick raises an exception when called if no handlers are registered."""

        brick = zBrick()
        with pytest.raises(NotImplementedError) as e:
            brick()

        assert e.match("ot intended for use as a callable")
    
    def test_handler_is_called_when_expected(self):
        """A zBrick calls the handler which matches the signature"""

        class TestBrick(zBrick):
        
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
        class GreeterBrick(zBrick):        

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
        class FakeWsgiBrick(zBrick):
        
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