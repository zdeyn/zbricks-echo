
from .flask import zFlaskBrick
from .base import zFlaskExtensionBrick, zFlaskBlueprintBrick

def create_flask(*args, **kwargs) -> zFlaskBrick:
    return zFlaskBrick(*args, **kwargs)
