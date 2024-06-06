from typing import Any, List, Type
import pytest
from pytest_bdd.exceptions import NoScenariosFound
from pytest_bdd import scenarios, given, when, then, parsers
from flask.testing import FlaskClient
from werkzeug.wrappers import Request, Response
from zbricks import zEventDispatcher

from rich import print

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from zbricks.events import zEvent, zSampleEvent, ANY

try:
    scenarios('features/events/')
except NoScenariosFound:
    pass

@pytest.fixture(scope='function')
def storage():
    return {}

@pytest.fixture(scope='function')
@given(parsers.parse('an event dispatcher'))
def _(storage):
    storage['dispatcher'] = zEventDispatcher()
    storage['handlers'] = {}
    storage['handler_calls'] = []
    return storage

@given(parsers.parse('a handler'))
def _(storage):
    storage['handlers'] = storage.get('handlers', {})
    storage['handler_calls'] = storage.get('handler_calls', [])

    def test_handler(event : zEvent):
        # nonlocal storage
        logger.debug(f"Test handler: event = '{event}'")
        storage['handler_calls'].append( ('test_handler', event) )
    
    storage['handlers']['test'] = test_handler

@given(parsers.parse('the handler is subscribed to "{event_type}" events'))
def _(event_type: str, storage : dict):
    dispatcher : zEventDispatcher = storage['dispatcher']
    cls = zEventDispatcher.event_class_from_name(event_type)
    assert issubclass(cls, zEvent)

    handler = storage['handlers']['test']
    
    # logger.debug(f"Subscribing, handler = '{handler}', event_type = '{event_type}'")
    dispatcher.subscribe(handler, cls)

@given(parsers.parse('a handler named "{handler_name}" subscribed to "{event_type}" events'))
def _(storage : dict, handler_name: str, event_type):

    storage['handlers'] = storage.get('handlers', {})
    storage['handler_calls'] = storage.get('handler_calls', [])

    def _(event : zEvent):
        # nonlocal storage
        logger.debug(f"Handler '{handler_name}' : event = '{event}'")
        storage['handler_calls'].append( (handler_name , event) )

    dispatcher : zEventDispatcher = storage['dispatcher']
    cls = zEventDispatcher.event_class_from_name(event_type)
    assert issubclass(cls, zEvent)
    
    storage['handlers'][handler_name] = _
    
    # logger.debug(f"Subscribing, handler = '{_}', event_type = '{event_type}'")
    dispatcher.subscribe(_, cls)


@when(parsers.parse('I send "{event_type}" with its "{property_key}" property set to "{property_value}"'))
def _(storage, event_type, property_key, property_value):
    dispatcher : zEventDispatcher = storage['dispatcher']
    cls = dispatcher.event_class_from_name(event_type)
    d = {}
    d[property_key] = property_value
    event = cls(**d)

    # logger.debug(f"Sending event, event = {event}")

    replies = dispatcher(event)
    storage['replies'] = storage.get('replies', [])
    storage['replies'].append( replies )


@then(parsers.parse('the handler should recieve "{event_type}" with its "{property_key}" property set to "{property_value}"'))
def _(storage, event_type, property_key, property_value):
    logger.debug(f"\nthe handler should recieve '{event_type}' with its '{property_key}' property set to '{property_value}'")

    assert len(storage['handler_calls']) > 0
    for name, event in storage['handler_calls']:
        assert name == 'test_handler'
        expecting_cls = zEventDispatcher.event_class_from_name(event_type)
        recieved_cls = type(event)
        if issubclass(recieved_cls, expecting_cls):
            assert getattr(event, property_key) == property_value
            return True
        
    return False

@then(parsers.parse('the handler named "{handler_name}" should recieve "{event_type}" with its "{property_key}" property set to "{property_value}"'))
def _(storage, handler_name, event_type, property_key, property_value):
    logger.debug(f"\nthe handler named '{handler_name}' should recieve '{event_type}' with its '{property_key}' property set to '{property_value}'")

    assert len(storage['handler_calls']) > 0
    for name, event in storage['handler_calls']:
        if name != handler_name:
            continue
        expecting_cls = zEventDispatcher.event_class_from_name(event_type)
        recieved_cls = type(event)

        if issubclass(recieved_cls, expecting_cls):
            assert getattr(event, property_key) == property_value
            return True
        
    return False

@then(parsers.parse('the handler should not recieve "{event_type}"'))
def _(storage, event_type):
    logger.debug(f"\nthe handler should not recieve '{event_type}'")

    for name, event in storage['handler_calls']:
        expecting_cls = zEventDispatcher.event_class_from_name(event_type)
        recieved_cls = type(event)
            
        if issubclass(recieved_cls, expecting_cls):
            return False
        
    return True

