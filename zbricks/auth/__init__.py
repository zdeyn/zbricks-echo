import logging
from typing import Optional
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from .blueprint import auth_bp, save_token, update_token
from .models import User
from ..extensions import db, oauth, jwtm, login_manager

class zAuth:
    def __init__(self, app: Optional[Flask]):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        # app.logger.setLevel(logging.DEBUG)
        
        for m in [db, jwtm, login_manager, oauth]:
            # app.logger.debug(f'Initializing {m}')
            m.init_app(app)

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
            db: SQLAlchemy = app.extensions.get('sqlalchemy') # type: ignore
            stmt = select(User).where(User.id == user_id)
            user = db.session.execute(stmt).scalar_one_or_none()
            app.logger.debug(f'Loaded user {user}')
            return user

        app.register_blueprint(auth_bp, url_prefix='/auth')
