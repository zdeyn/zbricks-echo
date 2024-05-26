from flask import Flask
from config import DevelopmentConfig
from zbricks.auth import zAuth

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    zauth = zAuth(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=True)
