from typing import Callable, Dict, List, Optional, Tuple, Type
import inspect
from dataclasses import dataclass, field

from zbricks.base import zBrick
from zbricks.augmentations import handler
from zbricks.events import zEvent, zSampleEvent, zRequestEvent

from rich import print

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)


# class zWsgiApplication(zBrick):    
#     _view_functions: Dict[str, Callable] = {}

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._view_functions = {}
#         self._zed = zEventDispatcher(name='wsgi')
#         self._zed.subscribe(self._handle_request_event, zRequestEvent)

#     def route(self, rule):
#         def decorator(f):
#             self._view_functions[rule] = f
#             return f
#         return decorator

#     @handler('call', types=(Dict, Callable))
#     def __wsgi_to_event(self, environ : Dict, start_response : Callable):
#         request = Request(environ)
#         path = request.path
#         view_function = self._view_functions.get(path)
#         if view_function: # resolve through direct routes first
#             response = view_function(request)
#         else:
#             ev = zRequestEvent(request = request)
#             replies = self._zed(ev)
#             if replies:
#                 response = replies[0]
#             else:
#                 response = Response(f'404 Not Found: {path}', status=404)
#         return response(environ, start_response)
    
#     def _handle_request_event(self, event: zRequestEvent):
#         request = event.request
#         path = request.path # type: ignore
#         view_function = self._view_functions.get(path)
#         if view_function: # resolve through direct routes first
#             response = view_function(request)
#         else:
#             response = Response(f'404 Not Found: {path}', status=404)
#         return response

#     def run(self, host='localhost', port=5000, **kwargs):
#         if kwargs.get('use_reloader', False):
#             print(f"zBricks: Reloader engaged!")
#         run_simple(host, port, self, **kwargs)

# if __name__ == '__main__':
#     # Create an instance of the zWsgiApplication class
#     app = zWsgiApplication(name='wsgi')
#     # Run the application at http://localhost:5000/
#     app.run()
