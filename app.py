import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from config import DevelopmentConfig
from zbricks import zApp, Response
from zbricks.auth.blueprint import auth_bp
from zbricks.extensions import db, oauth, jwtm, login_manager
# from zbricks.admin.blueprint import admin_bp

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.setLevel(logging.DEBUG)
    
    for m in [db, jwtm, login_manager, oauth]:
        app.logger.debug(f'Initializing {m}') 
        m.init_app(app)

    from zbricks.auth.blueprint import save_token, update_token
    from zbricks.auth.models import User

    oauth.register(
        'discord',
        client_id = app.config['DISCORD_CLIENT_ID'],
        client_secret = app.config['DISCORD_CLIENT_SECRET'],
        authorize_url = 'https://discord.com/api/oauth2/authorize',
        access_token_url = 'https://discord.com/api/oauth2/token',
        refresh_token_url= 'https://discord.com/api/oauth2/token',
        api_base_url = 'https://discord.com/api/',
        save_token=lambda token: save_token(token, user), # type: ignore
        auto_update_token={
            'update_token': update_token,
            'update_token_url': 'https://discord.com/api/oauth2/token',
        },
        client_kwargs = {'scope': 'identify email'}
    )

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        db : SQLAlchemy = app.extensions.get('sqlalchemy')

        stmt = select(User).where(User.id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        app.logger.debug(f'Loaded user {user}')
        return user
        # return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(admin_bp, url_prefix='/admin')  
    
    return app



# def create_app():
#     app = zApp(__name__)

#     @app.route('/')
#     def index():
#         return Response('Hello World!')

#     return app

if __name__ == '__main__':
    app = create_app()
    app.run(use_reloader=True)