from ....base import zAttachableMixin
from ....core import zBrick

# from .flask import zFlaskBrick
from flask import Flask, Blueprint

class zFlaskBlueprintBrick(Blueprint, zBrick):
    _name = 'zFlaskBlueprintBrick'

    def __init__(self, *args, **kwargs):
        # print(f"\nzFlaskBlueprintBrick initialized with: {args}, {kwargs}")
        Blueprint.__init__(self, 'bp', *args, import_name=__name__, **kwargs)
        zBrick.__init__(self, *args, **kwargs)

    def _attach_parent(self, parent: zAttachableMixin) -> None:

        # raise NotImplementedError("zFlaskBlueprintBrick._attach_parent")

        if not isinstance(parent, Flask):
            raise ValueError(f"Invalid parent: {parent}")

        # bp = Blueprint(self.name, parent.import_name)

        self._setup_routes()

        parent.register_blueprint(self, url_prefix='')

    def _setup_routes(self):

        @self.route('/hello-world-blueprint')
        def index():
            return 'Hello, World! (love, Blueprint)'
