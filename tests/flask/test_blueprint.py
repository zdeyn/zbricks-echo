# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick, create_flask_brick
from zbricks.bricks.flask import zFlaskBlueprintBrick

from flask import Flask, Blueprint

class Test_FlaskBlueprintBrick_Instance:

    @pytest.fixture(scope='class')
    def flask(self):
        return zFlaskBrick()
    
    @pytest.fixture(scope='class')
    def blueprint(self):
        return zFlaskBlueprintBrick()

    def test_exists(self, blueprint:zFlaskBlueprintBrick):
        assert blueprint is not None
    
    def test_is_blueprint(self, blueprint):
        assert isinstance(blueprint, Blueprint)
    
    def test_is_zbrick(self, blueprint):
        assert isinstance(blueprint, zBrick)

class Test_Example_FlaskBlueprintBrick_App:
    def test_works(self):
        app = create_flask_brick()
        bp = zFlaskBlueprintBrick()
        app.attach(bp)
        client = app.test_client()
        response = client.get('/hello-world-blueprint')
        decoded = response.data.decode('utf-8')
        assert 'Hello, World!' in decoded
        assert 'Blueprint' in decoded
