# zbricks/__init__.py
from .attachable import zAttachableMixin

from flask import Flask

class zFlaskBrick(Flask, zAttachableMixin):
    def __init__(self, **kwargs):
        if 'import_name' not in kwargs:
            kwargs['import_name'] = __name__
        super().__init__(**kwargs)
        
        @self.route('/')
        def index():
            return 'Hello, World!'

def create_flask_brick():
    app = zFlaskBrick()
    return app