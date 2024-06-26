# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick
from zbricks.bricks.flask import zFlaskExtensionBrick

from flask import Flask, Blueprint

@pytest.fixture(scope='class')
def flask():
    return zFlaskBrick()

@pytest.fixture(scope='class')
def extension():
    return zFlaskExtensionBrick()

class Test_zFlaskExtensionBrick_Instance:

    def test_exists(self, extension:zFlaskExtensionBrick):
        assert extension is not None
    
    def test_is_extension(self, extension):
        assert isinstance(extension, zFlaskExtensionBrick)

class Test_zFlaskExtensionBrick_Example:

    def test_works(self, flask: zFlaskBrick, extension: zFlaskExtensionBrick):
        app = flask
        app.attach(extension)
        client = app.test_client()
        response = client.get('/hello-world-extension')
        decoded = response.data.decode('utf-8')
        assert 'Hello, World!' in decoded
        assert 'Extension' in decoded
