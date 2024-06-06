from typing import Callable, Dict, List, Optional, Tuple, Type
import inspect
from dataclasses import dataclass, field
from pytest import Class, Function
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

from zbricks.base import handler, zBrick, zCallableAugmentation
from zbricks.events import zEvent, zSampleEvent, zRequestEvent

from rich import print

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

@dataclass
class zEventSubscription:
    cls : Type[zEvent]

class zEventDispatcher(zCallableAugmentation, zBrick):
    _event_subscriptions: Dict[Callable, List[zEventSubscription]] = {}
    _name: Optional[str] = None

    def __init__(self, name: Optional[str] = None, **kwargs):
        if name is None:
            name = self.__class__.__name__
        self._name = name
        self._event_subscriptions = {}

        super().__init__(**kwargs)

    @classmethod
    def event_class_from_name(cls, name: str) -> Type:    
        match name:
            case 'zEvent':
                return zEvent
            case 'zSampleEvent':
                return zSampleEvent
            case _:
                raise ValueError(f"Unknown event type: {name}")

    def subscribe(self, f: Callable, sub_to: Optional[Type[zEvent]] = zEvent):
        if sub_to is None:
            sub_to = zEvent
        logger.debug(f"\nzEventDispatcher: Subscribing handler '{f}' to event type '{sub_to}'")
        if f not in self._event_subscriptions:
            self._event_subscriptions[f] = []
        subscription = zEventSubscription(sub_to)
        self._event_subscriptions[f].append(subscription)
        logger.debug(f"\nSubscriptions:")
        for handler, subscriptions in self._event_subscriptions.items():
            logger.debug(f"handler: '{handler}', subscriptions: '{subscriptions}'")
        logger.debug(f"\n")
    
    def sub(self, *args):
        if len(args) == 1 and inspect.isclass(args[0]):
            event_type = args[0]
            def decorator(func):
                self.subscribe(func, event_type)
                return func
            return decorator
        else:
            func = args[0]
            self.subscribe(func)
            return func


    @handler('call', type=zEvent)
    def _handler(self, event: zEvent):
        replies = []
        logger.debug(f"\nzEventDispatcher: Sending event '{event}' to subscribers:")
        for handler, subscriptions in self._event_subscriptions.items():
            for subscription in subscriptions:
                if isinstance(event, subscription.cls):
                    logger.debug(f"\nzEventSubscription: Sending event '{event}' to handler '{handler}'")
                    reply = handler(event)
                    logger.debug(f"Got reply: '{reply}'")
                    replies.append(reply)

        logger.debug(f"Total replies '{replies}'")
        return replies


class zWsgiApplication(zCallableAugmentation, zBrick):
    _view_functions: Dict[str, Callable] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._view_functions = {}
        self._zed = zEventDispatcher(name='wsgi')
        self._zed.subscribe(self._handle_request_event, zRequestEvent)

    def route(self, rule):
        def decorator(f):
            self._view_functions[rule] = f
            return f
        return decorator

    @handler('call', types=(Dict, Callable))
    def __wsgi_to_event(self, environ : Dict, start_response : Callable):
        request = Request(environ)
        path = request.path
        view_function = self._view_functions.get(path)
        if view_function: # resolve through direct routes first
            response = view_function(request)
        else:
            ev = zRequestEvent(request = request)
            replies = self._zed(ev)
            if replies:
                response = replies[0]
            else:
                response = Response(f'404 Not Found: {path}', status=404)
        return response(environ, start_response)
    
    def _handle_request_event(self, event: zRequestEvent):
        request = event.request
        path = request.path
        view_function = self._view_functions.get(path)
        if view_function: # resolve through direct routes first
            response = view_function(request)
        else:
            response = Response(f'404 Not Found: {path}', status=404)
        return response

    def run(self, host='localhost', port=5000, **kwargs):
        if kwargs.get('use_reloader', False):
            print(f"zBricks: Reloader engaged!")
        run_simple(host, port, self, **kwargs)

if __name__ == '__main__':
    # Create an instance of the zWsgiApplication class
    app = zWsgiApplication(name='wsgi')
    # Run the application at http://localhost:5000/
    app.run()
