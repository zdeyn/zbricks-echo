# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick
from zbricks.bricks.templating import zTemplatingBrick

from flask import Flask, Blueprint

@pytest.fixture(scope='class')
def flask():
    return zFlaskBrick()

@pytest.fixture(scope='class')
def brick():
    from zbricks.bricks.templating import templating
    return templating

class Test_zTemplatingBrick_Instance:

    def test_exists(self, brick:zTemplatingBrick):
        assert brick is not None
    
    def test_is_blueprint(self, brick):
        assert isinstance(brick, Blueprint)
    
    def test_is_zbrick(self, brick):
        assert isinstance(brick, zBrick)

class Test_zTemplatingBrick_Example:
    def test_works(self, flask: zFlaskBrick, brick: zTemplatingBrick):
        app = flask
        bp = brick
        app.attach(bp)
        client = app.test_client()
        response = client.get('/hello-world-templating')
        decoded = response.data.decode('utf-8')
        assert 'Hello, World!' in decoded
        assert 'Templating' in decoded
