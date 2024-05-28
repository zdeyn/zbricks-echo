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
    
    storage['handler'] = test_handler

@given(parsers.parse('the handler is subscribed to "{event_type}" events'))
def _(event_type: str, storage : dict):
    dispatcher : zEventDispatcher = storage['dispatcher']
    cls = zEventDispatcher.event_class_from_name(event_type)
    assert issubclass(cls, zEvent)
    
    logger.debug(f"Subscribing, handler = '{storage['handler']}', event_type = '{event_type}'")
    dispatcher.subscribe(cls, storage['handler'])

@given(parsers.parse('a handler named "{handler_name}" subscribed to "{event_type}" events'))
def _(app: zApp, storage : dict, handler_name: str, event_type):
    storage['app'] = app
    storage['dispatcher'] = app.extensions['zevent']
    storage['handler_calls'] = []

    cls = zEventDispatcher.event_class_from_name(event_type)

    def handler(sender, event : zEvent):
        msg = f"Handled by {handler_name}"
        logger.debug(f"Handler {handler_name}, msg = '{msg}', sender = '{sender}', event = '{event}'")        
        storage['handler_calls'].append( (msg, sender, event) )

    storage['handlers'][handler_name] = handler

    storage['dispatcher'].subscribe(cls, handler)    


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


@then(parsers.parse('the handler should recieve "{event_type}" with its "{property_key}" property set to "{property_value}"'))
def _(storage, event_type, property_key, property_value):
    logger.debug(f"\nthe handler should recieve '{event_type}' with its '{property_key}' property set to '{property_value}'")

    assert len(storage['handler_calls']) > 0
    for msg, sender, event in storage['handler_calls']:
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
    for msg, sender, event in storage['handler_calls']:
        expecting_cls = zEventDispatcher.event_class_from_name(event_type)
        recieved_cls = type(event)

        if issubclass(recieved_cls, expecting_cls):
            assert getattr(event, property_key) == property_value
            return True
        
    return False

@then(parsers.parse('the handler should not recieve "{event_type}"'))
def _(storage, event_type):
    logger.debug(f"\nthe handler should not recieve '{event_type}'")

    for msg, sender, event in storage['handler_calls']:
        expecting_cls = zEventDispatcher.event_class_from_name(event_type)
        recieved_cls = type(event)
            
        if issubclass(recieved_cls, expecting_cls):
            return False
        
    return True

