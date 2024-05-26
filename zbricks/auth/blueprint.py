# auth.py

from rich import print
import logging

from flask import Flask, get_flashed_messages, session, flash, Blueprint, current_app, json, redirect, render_template_string, url_for, request, jsonify
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, verify_jwt_in_request
from authlib.integrations.flask_client import FlaskOAuth2App # type: ignore
from flask_login import login_user, logout_user, login_required, current_user # type: ignore

from .models import User # ,DiscordProfile
from .signals import NEW_USER_CREATED

auth_bp = Blueprint('auth', __name__)

def save_token(token, user: User):
    db : SQLAlchemy = current_app.extensions.get('sqlalchemy') # type: ignore
    user.access_token = token['access_token']
    user.refresh_token = token.get('refresh_token')
    db.session.commit()

    current_app.logger.debug(f'Saved token for user {user.username}')

def update_token(token, refresh_token=None, access_token=None):
    db : SQLAlchemy = current_app.extensions.get('sqlalchemy') # type: ignore

    stmt = select(User).where(User.access_token == token['access_token'])
    user = db.session.execute(stmt).scalar_one_or_none()

    if user:
        user.access_token = token['access_token']
        user.refresh_token = token.get('refresh_token', user.refresh_token)
        db.session.commit()    

        current_app.logger.debug(f'Updated token for user {user.username}')
    else:
        current_app.logger.error(f'Could not find user for token {token}')

@auth_bp.route('/')
def index():
    flash_data = get_flashed_messages(with_categories=True, category_filter=['success'])
    login_uri = url_for('.login')
    logout_uri = url_for('.logout')
    out = ''
    out += f'<h3>Flash: {flash_data}</h3>'
    out += f'<h1>Auth Blueprint</h1>'
    out += f'<a href="{login_uri}">Login</a>'
    out += f'<br/><a href="{logout_uri}">Logout</a>'

    if current_user.is_authenticated:
        out += f'<p>Current User Name: {current_user.username}</p>'
        out += f'<p>Current User ID: {current_user.id}</p>'
        out += f'<p>Current User Discord ID: {current_user.discord_id}</p>'
    else:
        out += f'<p>Not logged in</p>'

    return out

@auth_bp.route('/login')
def login():
    discord : FlaskOAuth2App = current_app.extensions.get('authlib.integrations.flask_client').discord

    redirect_uri = url_for('.authorize', _external=True)
    return discord.authorize_redirect(redirect_uri)    

@auth_bp.route('/logout')
def logout():
    response = jsonify({'logout': True})
    response.delete_cookie('access_token_cookie')
    response.status_code = 302
    response.headers['Location'] = url_for('.index')
    logout_user()
    return response

@auth_bp.route('/authorize')
def authorize():
    discord : FlaskOAuth2App = current_app.extensions.get('authlib.integrations.flask_client').discord
    db : SQLAlchemy = current_app.extensions.get('sqlalchemy')

    token = discord.authorize_access_token()

    profile_data = discord.get('users/@me')

    if hasattr(profile_data, 'json'):
        profile_data = profile_data.json()
        
    stmt = select(User).where(User.discord_id == profile_data['id'])
    user = db.session.execute(stmt).scalar_one_or_none()

    if not user:
        user = User(
            discord_id=profile_data['id'], 
            username=profile_data['username'],
            is_authenticated=True            
            )
        db.session.add(user)
        NEW_USER_CREATED.send(current_app._get_current_object(), user=user, profile=profile_data)

    save_token(token, user)

    # Create JWT and set it in cookies
    access_token = create_access_token(identity=user.id)
    response = jsonify({'login': True})
    set_access_cookies(response, access_token)    
    login_user(user, remember=True)
    # response.status_code = 302
    # response.headers['Location'] = url_for('.index')

    flash(message = 'Logged in successfully', category='success')

    next = session.pop('next', None)
    
    # url_has_allowed_host_and_scheme should check if the url is safe
    # for redirects, meaning it matches the request host.
    # See Django's url_has_allowed_host_and_scheme for an example.
    # if not url_has_allowed_host_and_scheme(next, request.host):
    #     return flask.abort(400)

    return redirect(next or url_for('.index'))

@auth_bp.route("/protected")
@login_required
def protected():
    return render_template_string(
        "Flash: {{flash_data}}<br/>Logged in as: {{ user.username }}",
        flash_data=get_flashed_messages(),
        user=current_user
    )



@NEW_USER_CREATED.connect
def test_new_user_created_signal(sender, **extra):
    print(f'Sender {sender} sent {extra}')