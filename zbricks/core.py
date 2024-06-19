
from zbricks.base import zAttachableMixin

class zBrick(zAttachableMixin):
    def __repr__(self) -> str:
        return f"zBrick(name={self._name})"
