from typing import Optional
from flask import Flask, get_flashed_messages, url_for

from jinja2 import PackageLoader, ChoiceLoader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import current_user

from .blueprint import auth_bp, save_token, update_token
from .models import User
from ..extensions import db, oauth, jwtm, login_manager

from ..logging import zbricks_logger
logger = zbricks_logger('zAuth')

class zAuth:
    _app : Optional[Flask] = None

    def __init__(self, app: Optional[Flask] = None):
        logger.zext(f"Creating zAuth, app = '{app}'")

        if app is not None:
            logger.debug(f"Configuring zAuth")
            self.init_app(app)
        logger.zext(f"Finalized zAuth")
    
    def init_app(self, app: Flask):
        logger.zext(f"Configuring zAuth, app = '{app}'")

        self._app = app
        app.extensions['zauth'] = self

        app.jinja_loader = ChoiceLoader([
            app.jinja_loader, # type: ignore
            PackageLoader('zbricks.auth', 'templates'),
            PackageLoader('zbricks', 'templates')
        ])
        
        for m in [db, jwtm, login_manager, oauth]:
            logger.debug(f"Initalizing extension '{m}'")
            m.init_app(app)

        logger.debug(f"Configuring OAuth provider 'discord'")
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

        logger.debug(f"Configuring JWT manager")
        login_manager.login_view = ".login"

        @login_manager.user_loader
        def load_user(user_id):
            db: SQLAlchemy = app.extensions.get('sqlalchemy') # type: ignore
            stmt = select(User).where(User.id == user_id)
            user = db.session.execute(stmt).scalar_one_or_none()
            app.logger.debug(f'Loaded user {user}')
            return user
        
        logger.debug(f"Configuring context processor 'inject_navigation'")
        @app.context_processor
        def inject_navigation():

            login_uri = url_for('auth.login')
            logout_uri = url_for('auth.logout')
            # dashboard_uri = url_for('dashboard')
            dashboard_uri = url_for('auth.protected')

            if current_user.is_authenticated:
                links = [
                    ('Home', url_for('index')),
                    ('Dashboard', dashboard_uri),
                    ('Log Out', logout_uri),
                ]
            else:
                links = {
                    ('Home', url_for('index')),
                    ('Log In', login_uri),
                }
            return {'navigation': links}

        logger.zext(f"Registering blueprint 'auth', url_prefix = '/auth'")
        app.register_blueprint(auth_bp, url_prefix='/auth')
