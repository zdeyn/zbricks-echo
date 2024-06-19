from ...core import zBrick
from .blueprint import zFlaskBlueprintBrick
from flask import Flask

class zFlaskBrick(Flask, zBrick):
    def __init__(self, *args, **kwargs):
        # print(f"\nzFlaskBrick initialized with: {args}, {kwargs}")
        Flask.__init__(self, __name__, *args, **kwargs)
        zBrick.__init__(self, *args, **kwargs)
        
        # @self.route('/')
        # def index():
        #     return 'Hello, World!'

def create_flask_brick():
    app = zFlaskBrick()
    bp = zFlaskBlueprintBrick()
    app.attach(bp)
    return app