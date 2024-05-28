from flask import Flask, render_template, get_flashed_messages, current_app
from config import DevelopmentConfig
from zbricks import zApp

from zbricks.logging import zbricks_logger

logger = zbricks_logger(__name__)

def create_app(config_class=DevelopmentConfig):

    logger.debug(f"create_app: Creating app, name = '{__name__}', config_class = '{config_class}'")
    app = zApp(__name__, config_class=config_class)

    @app.route('/')
    def index():
        flash_data = get_flashed_messages(with_categories=True, category_filter=['success'])
        return render_template('index.html', content="Woot!")
    
    logger.debug(f"create_app: Finalized app, name = '{__name__}'")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=True)
