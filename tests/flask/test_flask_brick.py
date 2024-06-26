# tests/test_zbrick.py
import pytest
from zbricks import zBrick, zFlaskBrick

from flask import Flask

class Test_zFlaskBrick_Instance:

    @pytest.fixture(scope='class')
    def flask(self):
        return zFlaskBrick()

    def test_exists(self, flask:Flask):
        assert flask is not None
    
    def test_is_flask(self, flask):
        assert isinstance(flask, Flask)
    
    def test_is_zbrick(self, flask):
        assert isinstance(flask, zBrick)

class Test_zFlaskBrick_Example:
    def test_create(self):
        app = zFlaskBrick()
        app.config.from_object('config.TestingConfig')
        assert isinstance(app, Flask)
    
    # def test_routing(self):
    #     app = create_flask_brick()
    #     client = app.test_client()
    #     response = client.get('/')
    #     decoded = response.data.decode('utf-8')
    #     assert 'Hello, World!' in decoded
    #     # assert 'zBricks' in decoded
