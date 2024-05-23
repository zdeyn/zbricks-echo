import pytest
from unittest.mock import patch

from zbricks.core.events import zEvent, event
from zbricks.core.zmachine import zMachine


def test_no_event_handlers():
    
    zEvent._reset()
    results = zEvent.fire()
    assert results == []


def test_basic_connect():
    
    zEvent._reset()

    def basic_connect_handler(*args, **kwargs):
        return f'basic connect: args={args}, kwargs={kwargs}'
    
    zEvent.connect(basic_connect_handler)
    results = zEvent.fire()

    assert results == [
        [(zEvent, basic_connect_handler, (), {}) , 'basic connect: args=(), kwargs={}'],
    ]

def test_subclass_fires_parent():
    
    zEvent._reset()

    class zEventSubclass(zEvent): pass
    
    def connect_subclass_handler(*args, **kwargs):
        return f'connect subclass: args={args}, kwargs={kwargs}'
    
    zEvent.connect(connect_subclass_handler)
    results = zEventSubclass.fire()

    assert results == [
        [(zEventSubclass, connect_subclass_handler, (), {}) , 'connect subclass: args=(), kwargs={}'],
    ]


# @pytest.mark.skip("Decorator not implemented")
def test_basic_decorator():
    
    zEvent._reset()
    
    @event
    def basic_decorator_handler(*args, **kwargs):
        return f'basic decorator: args={args}, kwargs={kwargs}'
    
    results = zEvent.fire()

    assert results == [
        [(zEvent, basic_decorator_handler, (), {}), 'basic decorator: args=(), kwargs={}']
    ]

# @pytest.mark.skip("Decorator not implemented")
def test_decorator_with_args():
    
    @event('foo', bar='baz')
    def quzz(*args, **kwargs):
        return f'decorator with args: args={args}, kwargs={kwargs}'
    
    results = zEvent.fire()

    assert results == [
        [(zEvent, quzz, (), {}), "decorator with args: args=('foo',), kwargs={bar: 'baz'}"]
    ]