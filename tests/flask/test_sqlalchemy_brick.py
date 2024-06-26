# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick
from zbricks.bricks.sqla import zSQLAlchemyBrick
from sqlalchemy.orm import Mapped, mapped_column

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture(scope='class')
def flask() -> zFlaskBrick:
    return zFlaskBrick()

@pytest.fixture(scope='class')
def sqlalchemy() -> zSQLAlchemyBrick:
    from zbricks.bricks.sqla import db
    return db

class Test_zSQLAlchemyBrick_Instance:

    def test_exists(self, sqlalchemy:zSQLAlchemyBrick):
        assert sqlalchemy is not None
    
    def test_is_sqlalchemy(self, sqlalchemy:SQLAlchemy):
        assert isinstance(sqlalchemy, SQLAlchemy)
    
    def test_is_zbrick(self, sqlalchemy: zBrick):
        assert isinstance(sqlalchemy, zBrick)

class Test_zSQLAlchemyBrick_Example:
    def test_works(self, flask: zFlaskBrick):
        app = flask
        app.config.from_object('config.TestingConfig')

        from zbricks.bricks.flask.extensions.sqlalchemy import db, BaseModel
        app.attach(db)

        assert isinstance(app, Flask)
        assert isinstance(db, SQLAlchemy)

        class _TestUser(BaseModel):
            id: Mapped[int] = mapped_column(primary_key=True)
            username: Mapped[str] = mapped_column(unique=True)
            email: Mapped[str]
        
        with app.app_context():
            db.create_all()
            user : _TestUser = _TestUser(username='admin', email='zdeyn@zdeyn.com')
            assert user.username == 'admin'
            db.session.add(user)
            db.session.commit()

