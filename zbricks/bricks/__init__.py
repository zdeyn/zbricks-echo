from typing import Callable, Dict, Tuple
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

from zbricks.base import call_handler, zBrick, zCallableAugmentation

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
