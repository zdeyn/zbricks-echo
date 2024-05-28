from typing import Any, List, Type
import pytest
from pytest_bdd.exceptions import NoScenariosFound
from pytest_bdd import scenarios, given, when, then, parsers
from flask.testing import FlaskClient
from werkzeug.wrappers import Request, Response
from zbricks import zApp, zEventDispatcher
from flask import Flask

from rich import print

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from zbricks.events import zEvent, zSampleEvent, ANY

try:
    scenarios('features/events/')
except NoScenariosFound:
    pass

@given(parsers.parse('a handler'))
def _(app : zApp, storage : dict):
    storage['app'] = app
    storage['dispatcher'] = app.extensions['zevent']
    storage['handler_calls'] = []

    def test_handler(sender, event : zEvent):
        msg = f"Handled by test_handler"
        logger.debug(f"Test handler, msg = '{msg}', sender = '{sender}', event = '{event}'")
        storage['handler_calls'].append( (msg, sender, event) )
        return Response(msg, status=200, content_type='text/plain')
    
    # logger.zevent(f"Creating to event type '{event_type}'")
    storage['handler'] = test_handler
    # logger.debug(f"STORAGE: {storage}")

@given(parsers.parse('the handler is subscribed to "{event_type}" events'))
def _(event_type: str, storage : dict):
    dispatcher : zEventDispatcher = storage['dispatcher']
    cls = dispatcher.event_class_from_name(event_type)
    assert issubclass(cls, zEvent)
    
    logger.debug(f"Subscribing, handler = '{storage['handler']}', event_type = '{event_type}'")
    dispatcher.subscribe(cls, storage['handler'])


@when(parsers.parse('I send "{event_type}" with its "{property_key}" property set to "{property_value}"'))
def _(storage, event_type, property_key, property_value):
    dispatcher : zEventDispatcher = storage['dispatcher']
    cls = dispatcher.event_class_from_name(event_type)
    d = {}
    d[property_key] = property_value
    event = cls(**d)

    logger.debug(f"Sending event, event = {event}")

    replies = dispatcher.send_event(event)
    storage['replies'].append( replies )


@then(parsers.parse('the subscriber should receive "{event_type}" with its "{property_key}" property set to "{property_value}"'))
def _(storage, event_type, property_key, property_value):
    logger.debug(f"\nthe subscriber should receive '{event_type}' with its '{property_key}' property set to '{property_value}'")
    # print(f"\nHandler calls: {storage['handler_calls']}")
    #storage['handler_calls'].append( (msg, sender, event) )

    assert len(storage['handler_calls']) > 0
    for msg, sender, event in storage['handler_calls']:
        # print(f"\nCall: msg = '{msg}', sender = '{sender}', event = '{event}'")
        cls = zEventDispatcher.event_class_from_name(event_type)            
            
        if issubclass(cls, zEvent):
            assert event.name == event_type
            assert getattr(event, property_key) == property_value
            return True
        
    return False

@then(parsers.parse('the subscriber should not receive "{event_type}"'))
def _(storage, event_type):
    logger.debug(f"\nthe subscriber should not receive '{event_type}'")
    # print(f"\nNEGATIVE andler calls: {storage['handler_calls']}")
    #storage['handler_calls'].append( (msg, sender, event) )

    for msg, sender, event in storage['handler_calls']:
        # print(f"\nCall: msg = '{msg}', sender = '{sender}', event = '{event}'")
        cls = zEventDispatcher.event_class_from_name(event_type)            
            
        if sender != event_type:
            return False
        
    return True

