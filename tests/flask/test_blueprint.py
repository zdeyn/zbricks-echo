# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick
from zbricks.bricks.flask import zFlaskBlueprintBrick

from flask import Flask, Blueprint

@pytest.fixture(scope='class')
def flask():
    return zFlaskBrick()

@pytest.fixture(scope='class')
def blueprint():
    return zFlaskBlueprintBrick()

class Test_FlaskBlueprintBrick_Instance:

    def test_exists(self, blueprint:zFlaskBlueprintBrick):
        assert blueprint is not None
    
    def test_is_blueprint(self, blueprint):
        assert isinstance(blueprint, Blueprint)
    
    def test_is_zbrick(self, blueprint):
        assert isinstance(blueprint, zBrick)

class Test_Example_FlaskBlueprintBrick_App:
    def test_works(self, flask: zFlaskBrick, blueprint: zFlaskBlueprintBrick):
        app = flask
        bp = blueprint
        app.attach(bp)
        client = app.test_client()
        response = client.get('/hello-world-blueprint')
        decoded = response.data.decode('utf-8')
        assert 'Hello, World!' in decoded
        assert 'Blueprint' in decoded
