from ....base import zAttachableMixin
from ....core import zBrick

from flask import Flask

class zFlaskExtensionBrick(zBrick):
    _name = 'zFlaskExtension'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _attach_parent(self, parent: zAttachableMixin) -> None:

        # raise NotImplementedError("zFlaskBlueprintBrick._attach_parent")

        if not isinstance(parent, Flask):
            raise ValueError(f"Invalid parent: {parent}")

        self._setup_extension(parent)
    
    def _setup_extension(self, app: Flask) -> None:
        self.init_app(app)
        
        @app.route('/hello-world-extension')
        def index():
            return 'Hello, World! (love, Extension)'
        
    def init_app(self, app: Flask) -> None:
        if not isinstance(app, Flask):
            raise ValueError(f"Invalid app: {app}")

        
