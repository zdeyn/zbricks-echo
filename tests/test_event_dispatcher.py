# tests/test_auth_routes.py
from typing import Any, Callable, Iterable, Tuple, Union
import pytest

from unittest.mock import MagicMock
from flask import Flask, make_response
from rich import print
# from flask.testing import FlaskClient
from pytest_mock import MockFixture

from zbricks.base import zBrick, call_handler
from zbricks.bricks import zEventDispatcher, zEvent, zEventSubscription
from zbricks.bricks import zWsgiApplication
from werkzeug.wrappers import Request, Response
from werkzeug.test import Client

class Test_zEventDispatcher_Sub_Decorator:

    def test_notifies_subscriber_exact(self):
        calls = []

        zed = zEventDispatcher()

        @zed.sub
        def handler(event: zEvent):
            nonlocal calls
            calls.append( ('handler', event) )

        ev = zEvent()
        zed(ev)
        assert len(calls) == 1
        handler, event = calls[0]
        assert handler == 'handler'
        assert event is ev
    
    def test_filters_multiple_subscribers_subtype(self):
        class zSubEvent(zEvent): pass
        calls = []

        zed = zEventDispatcher()

        @zed.sub(zEvent)
        def called(event: zEvent):
            nonlocal calls
            calls.append( ('called', event) )

        @zed.sub(zSubEvent)
        def skipped(event: zSubEvent):
            nonlocal calls
            calls.append( ('skipped', event) )

        ev = zEvent()
        zed(ev)
        assert len(calls) == 1        
        assert calls[0] == ('called', ev)

class Test_zEventDispatcher_Subscribe:    

    # @pytest.mark.skip(reason="...")
    def test_can_instantiate(self):        
        zed = zEventDispatcher()

        assert zed is not None
    
    def test_can_subscribe(self):
        zed = zEventDispatcher()

        def handle_event(event: zEvent):
            pass

        zed.subscribe(handle_event)
        assert handle_event in zed._event_subscriptions
        assert len(zed._event_subscriptions[handle_event]) == 1
        assert zed._event_subscriptions[handle_event][0].cls == zEvent

    def test_notifies_subscriber_exact(self):
        calls = []

        zed = zEventDispatcher()

        def handler(event: zEvent):
            nonlocal calls
            calls.append( ('handler', event) )

        zed.subscribe(handler)
        ev = zEvent()
        zed(ev)
        assert len(calls) == 1
        handler, event = calls[0]
        assert handler == 'handler'
        assert event is ev
    
    def test_notifies_subscriber_subtype(self):
        class zSubEvent(zEvent): pass
        calls = []

        zed = zEventDispatcher()

        def handler(event: zEvent):
            nonlocal calls
            calls.append( ('handler', event) )

        zed.subscribe(handler) # default zEvent
        ev = zSubEvent()
        zed(ev)
        assert len(calls) == 1
        assert calls[0] == ('handler', ev)
    
    def test_notifies_multiple_subscribers(self):
        calls = []

        zed = zEventDispatcher()

        def one(event: zEvent):
            nonlocal calls
            calls.append( ('one', event) )

        def two(event: zEvent):
            nonlocal calls
            calls.append( ('two', event) )

        zed.subscribe(one)
        zed.subscribe(two)
        ev = zEvent()
        zed(ev)
        assert len(calls) == 2        
        assert calls[0] == ('one', ev)
        assert calls[1] == ('two', ev)
    
    def test_filters_on_subtype(self):
        class zSubEvent(zEvent): pass
        calls = []

        zed = zEventDispatcher()

        def handler(event: zSubEvent):
            nonlocal calls
            calls.append( ('handler', event) )

        zed.subscribe(handler, zSubEvent)
        ev = zEvent()
        zed(ev)
        assert len(calls) == 0 
    
    def test_filters_multiple_subscribers_subtype(self):
        class zSubEvent(zEvent): pass
        calls = []

        zed = zEventDispatcher()

        def called(event: zEvent):
            nonlocal calls
            calls.append( ('called', event) )

        def skipped(event: zSubEvent):
            nonlocal calls
            calls.append( ('skipped', event) )

        zed.subscribe(called)
        zed.subscribe(skipped, zSubEvent)
        ev = zEvent()
        zed(ev)
        assert len(calls) == 1        
        assert calls[0] == ('called', ev)
        