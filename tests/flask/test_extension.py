# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick, create_flask_brick
from zbricks.bricks.flask import zFlaskExtensionBrick

from flask import Flask, Blueprint

class Test_FlaskBlueprintBrick_Instance:

    @pytest.fixture(scope='class')
    def flask(self):
        return zFlaskBrick()
    
    @pytest.fixture(scope='class')
    def extension(self):
        return zFlaskExtensionBrick()

    def test_exists(self, extension:zFlaskExtensionBrick):
        assert extension is not None
    
    def test_is_extension(self, extension):
        assert isinstance(extension, zFlaskExtensionBrick)

class Test_Example_FlaskBlueprintBrick_App:
    def test_works(self):
        app = create_flask_brick()
        ext = zFlaskExtensionBrick()
        app.attach(ext)
        client = app.test_client()
        response = client.get('/hello-world-extension')
        decoded = response.data.decode('utf-8')
        assert 'Hello, World!' in decoded
        assert 'Extension' in decoded
