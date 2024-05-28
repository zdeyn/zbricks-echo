from flask import Flask, render_template, url_for, get_flashed_messages, current_app
from flask_login import current_user
from config import DevelopmentConfig
from zbricks.auth import zAuth

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    zauth = zAuth(app)

    @app.route('/')
    def index():
        flash_data = get_flashed_messages(with_categories=True, category_filter=['success'])
        return render_template('index.html', content="Woot!")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=True)
