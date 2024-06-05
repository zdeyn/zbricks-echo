from typing import Callable, Dict, List, Optional, Tuple, Type
import inspect
from dataclasses import dataclass, field
from pytest import Class, Function
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

from zbricks.base import call_handler, zBrick, zCallableAugmentation

from rich import print

@dataclass
class zEvent:
    pass

@dataclass
class zEventSubscription:
    cls : Type[zEvent]

class zEventDispatcher(zCallableAugmentation, zBrick):
    _event_subscriptions: Dict[Callable, List[zEventSubscription]] = {}

    def subscribe(self, f: Callable, cls: Optional[Type[zEvent]] = zEvent):
        if f not in self._event_subscriptions:
            self._event_subscriptions[f] = []
        if cls is None:
            cls = zEvent
        subscription = zEventSubscription(cls)
        self._event_subscriptions[f].append(subscription)
    
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


    @call_handler(zEvent)
    def _handler(self, event: zEvent):
        for handler, subscriptions in self._event_subscriptions.items():
            for subscription in subscriptions:
                if isinstance(event, subscription.cls):
                    handler(event)


class zWsgiApplication(zCallableAugmentation, zBrick):
    _view_functions: Dict[str, Callable] = {}

    def route(self, rule):
        def decorator(f):
            self._view_functions[rule] = f
            return f
        return decorator

    @call_handler(Dict, Callable)
    def _handler(self, environ : Dict, start_response : Callable):
        request = Request(environ)
        path = request.path
        view_function = self._view_functions.get(path)
        if view_function:
            response = view_function(request)
        else:
            response = Response(f'404 Not Found: {path}', status=404)
        return response(environ, start_response)

    def run(self, host='localhost', port=5000, **kwargs):
        if kwargs.get('use_reloader', False):
            print(f"zBricks: Reloader engaged!")
        run_simple(host, port, self, **kwargs)

if __name__ == '__main__':
    # Create an instance of the zWsgiApplication class
    app = zWsgiApplication(name='wsgi')
    # Run the application at http://localhost:5000/
    app.run()
