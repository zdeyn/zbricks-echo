
from zbricks.base import zAttachableMixin

class zBrick(zAttachableMixin):
    def __init__(self, *args, **kwargs):
        # print(f"\nzBrick initialized with: {args}, {kwargs}")
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"zBrick(name={self.name})"
