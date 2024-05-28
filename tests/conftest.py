# tests/conftest.py
import pytest
from typing import Any, Generator, List
from unittest.mock import MagicMock
from pytest_mock import MockFixture
from flask.testing import FlaskClient
from zbricks import zApp, Request, Response
from flask_sqlalchemy import SQLAlchemy

from config import TestingConfig
from app import create_app

@pytest.fixture
def app() -> Generator[zApp, None, None]:

    app : zApp = create_app(TestingConfig)
    app.testing = True        
    with app.app_context():
        assert app.config['TESTING'] == True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == TestingConfig.SQLALCHEMY_DATABASE_URI
        assert app.extensions.get('sqlalchemy') is not None
        db : SQLAlchemy = app.extensions.get('sqlalchemy') # type: ignore
        # db.engine.echo = True
        db.drop_all() 
        db.create_all()    
        yield app        


@pytest.fixture
def client(app : zApp) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client

@pytest.fixture
def storage(app : zApp) -> dict:
    return {
        'app': app,
        'request': Request|None, # type: ignore
        'response': Response|None, 
        'handler_calls': [],
        'replies': [],
    }

@pytest.fixture
def mock_discord(app : zApp, mocker: MockFixture) -> MagicMock:
    """A mock of the Discord OAuth client."""
    oauth = app.extensions['authlib.integrations.flask_client']
    mock_discord = mocker.patch.object(oauth, 'discord', spec=oauth.discord, return_value=MagicMock())
    return mock_discord

@pytest.fixture
def mock_db_session(app : zApp, mocker: MockFixture) -> MagicMock:
    """A mock of the database."""
    db = app.extensions.get('sqlalchemy')
    mock_db_session = mocker.patch.object(db, 'session', spec=getattr(db, 'session', None), return_value=MagicMock())
    return mock_db_session