from zbricks import zApp, Response

def create_app():
    app = zApp()

    @app.route('/')
    def index(request):
        return Response('Hello World!')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=True)