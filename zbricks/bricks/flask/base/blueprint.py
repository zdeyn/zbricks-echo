from ....base import zAttachableMixin
from ....core import zBrick

# from .flask import zFlaskBrick
from flask import Flask, Blueprint

class zFlaskBlueprintBrick(Blueprint, zBrick):
    _name = 'zFlaskBlueprintBrick'
    _prefix = ''

    def __init__(self, name = 'bp', prefix = '', import_name = None, *args, **kwargs):
        # print(f"\nzFlaskBlueprintBrick initialized with: {args}, {kwargs}")
        self.name = name
        self._prefix = prefix
        Blueprint.__init__(self, name, import_name or __name__, *args, **kwargs)
        zBrick.__init__(self, *args, **kwargs)

    def _attach_parent(self, parent: zAttachableMixin) -> None:

        # raise NotImplementedError("zFlaskBlueprintBrick._attach_parent")

        if not isinstance(parent, Flask):
            raise ValueError(f"Invalid parent: {parent}")

        # bp = Blueprint(self.name, parent.import_name)

        self._setup_routes()

        parent.register_blueprint(self, url_prefix=self._prefix)

    def _setup_routes(self):

        @self.route('/hello-world-blueprint')
        def index():
            return 'Hello, World! (love, Blueprint)'
