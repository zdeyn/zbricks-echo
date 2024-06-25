from ...core import zBrick
from .base import zFlaskBlueprintBrick
from flask import Flask

class zFlaskBrick(Flask, zBrick):
    def __init__(self, *args, **kwargs):
        # print(f"\nzFlaskBrick began init with: {args}, {kwargs}")
        import_name = kwargs.pop('import_name', __name__)
        config = kwargs.pop('config', None)
        children = kwargs.pop('children', [])
        # print(f"\nzFlaskBrick initialized with: {args}, {kwargs}")
        Flask.__init__(self, 
                    import_name, 
                    *args, 
                    # instance_relative_config=instance_relative_config,
        )
        if config:
            self.config.from_object(config)

        zBrick.__init__(self, *args, children=children, **kwargs)
