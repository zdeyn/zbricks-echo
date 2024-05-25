import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from typing import Generator
from unittest.mock import MagicMock
from pytest_mock import MockFixture
from flask.testing import FlaskClient
from zbricks import _zapp_class, zApp, Request, Response
from flask_sqlalchemy import SQLAlchemy

from config import TestingConfig  # Import the appropriate config
from app import create_app

@pytest.fixture
def app() -> Generator[_zapp_class, None, None]:

    # zapp = zApp(__name__)
    app = create_app()
    with app.app_context():
        db : SQLAlchemy = app.extensions.get('sqlalchemy')
        # db.engine.echo = True
        db.drop_all() 
        db.create_all()
        yield app        


@pytest.fixture
def client(app : _zapp_class) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_discord(app : _zapp_class, mocker: MockFixture) -> MagicMock:
    """A mock of the Discord OAuth client."""
    oauth = app.extensions['authlib.integrations.flask_client']
    mock_discord = mocker.patch.object(oauth, 'discord', spec=oauth.discord, return_value=MagicMock())
    return mock_discord

@pytest.fixture
def mock_db_session(app : _zapp_class, mocker: MockFixture) -> MagicMock:
    """A mock of the database."""
    db = app.extensions.get('sqlalchemy')
    mock_db_session = mocker.patch.object(db, 'session', spec=getattr(db, 'session', None), return_value=MagicMock())
    return mock_db_session