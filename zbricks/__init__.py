from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple


# class zEvent:

class zApp:
    def __init__(self, import_name = None):
        self._import_name = import_name
        self.url_map = Map()

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__)
            self.url_map.add(Rule(rule, endpoint=endpoint))
            setattr(self, endpoint, f)
            return f
        return decorator

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        urls = self.url_map.bind_to_environ(environ)
        try:
            endpoint, args = urls.match()
            response = getattr(self, endpoint)(**args)
        except Exception as e:
            response = self.handle_404()
        return response(environ, start_response)

    def handle_404(self):
        return Response('Not Found', status=404)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def run(self, host='localhost', port=5000, **kwargs):
        run_simple(host, port, self, **kwargs)