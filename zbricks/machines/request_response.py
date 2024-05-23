# zmachine/machines.py

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

import logging
from colorlog import ColoredFormatter

# Create a logger
logger = logging.getLogger('zbricks')
logger.setLevel(logging.CRITICAL)  # Set minimum logging level

# Create a handler (e.g., console handler)
ch = logging.StreamHandler()

# Define a formatter with line breaks and colors
formatter = ColoredFormatter(
    "\n%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# Set formatter to the handler
ch.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(ch)

from ..core.events import zEvent
from ..core.zmachine import zMachine

class zException(Exception):
    pass

class zUnknownMethodException(zException):
    pass

class zRequestEvent(zEvent):
    def __init__(self, request: Request) -> None:
        self.request = request

class zGetRequestEvent(zRequestEvent):
    pass

class zRequestResponseMachine(zMachine):
    def __init__(self) -> None:
        super().__init__()
    
        self.routes = {}
        self.errors = {}

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def error(self, path):
        def decorator(func):
            self.errors[path] = func
            return func
        return decorator

    def handle_request(self, request: Request) -> Response:
        logger.debug(f"Request: {request}, path = {request.path}")

        try:
            match request.method:
                case 'GET':
                    req_event = zGetRequestEvent(request)
                case _:
                    raise zUnknownMethodException(f"Unknown method: {request.method}")
                
        except zUnknownMethodException as exc:
            # logger.error(f"Unknown method: {exc}")
            return Response(f"Internal Server Error: {exc.__class__}", status=500)

        logger.debug(f"Request event: {req_event.__class__}, data = {req_event.request.path}")

        response = self.process_request_events(req_event)

        logger.debug(f"Response: {response}, data = {response.data}")

        return response

    def process_request_events(self, event: zRequestEvent) -> Response:
        match event:
            case zGetRequestEvent() if event.request.path in self.routes:
                return self.routes[event.request.path](event.request)
            case zGetRequestEvent() if 404 in self.errors:
                return self.errors[404](event.request)
            case _:
                return Response(f"Default 404 Error: {event.request.path}", status=404)

        
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def run(self, host='localhost', port=5000, use_reloader=False):
        run_simple(host, port, self.wsgi_app, use_reloader=use_reloader)