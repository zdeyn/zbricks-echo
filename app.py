from dotenv import load_dotenv
import os
from flask import Flask, render_template, get_flashed_messages, current_app
from werkzeug.wrappers import Request, Response
from config import DevelopmentConfig

from zbricks import zApp
from zbricks.bricks import zWsgiApplication

from zbricks.logging import zbricks_logger

logger = zbricks_logger(__name__)
logger.debug(f"Starting app.py")

def create_app(config_class=DevelopmentConfig):
    logger.debug(f"load_dotenv: Loading environment")
    load_dotenv()
        
    logger.debug(f"create_app: Creating app, name = '{__name__}', config_class = '{config_class}'")
    app = zApp(__name__, config_class=config_class)

    @app.route('/')
    def index():
        flash_data = get_flashed_messages(with_categories=True, category_filter=['success'])
        return render_template('index.html', content="Woot!")
    
    logger.debug(f"create_app: Finalized app, name = '{__name__}'")
    return app

def create_alt_app():
    load_dotenv()

    app = zWsgiApplication()

    @app.route('/')
    def index(request: Request):
        # see if name= is in the query string
        name = request.args.get('name', 'World')
        return Response(f'Hello, {name}!')
    return app

if __name__ == '__main__':
    # app = create_app()
    app = create_alt_app()
    app.run(use_reloader=True)
