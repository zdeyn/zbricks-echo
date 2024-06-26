from ..base import zFlaskExtensionBrick
from flask import Flask

from zbricks.bricks.sqla import Mapped, mapped_column
from zbricks.bricks.sqla import db, BaseModel

class zAuthenticationBrick(zFlaskExtensionBrick):
    _name = 'auth'

    def __init__(self, *args, **kwargs):
        print(f"\nzAuthenticationBrick initialized with: {args}, {kwargs}")
        zFlaskExtensionBrick.__init__(self, *args, **kwargs)

    def _attach_extension(self, app: Flask) -> None:
        pass

auth = zAuthenticationBrick()

class Credentials(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]