
from typing import Type, cast
from ..base import zFlaskExtensionBrick

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from typing import TYPE_CHECKING, TypeVar, Type
from flask_sqlalchemy.model import Model

class Base(Model):
  pass


class zSQLAlchemyBrick(SQLAlchemy, zFlaskExtensionBrick):
    _name = 'db'
    Model: Type[Base] # type: ignore

    def __init__(self, *args, **kwargs):
        print(f"\nzSQLAlchemyBrick initialized with: {args}, {kwargs}")        
        _model_class = kwargs.pop('model_class')
        SQLAlchemy.__init__(self, *args, model_class = _model_class, **kwargs)
        zFlaskExtensionBrick.__init__(self, *args, **kwargs)
        self.Model = self.Model

    def _attach_extension(self, app: Flask) -> None:
        self.init_app(app)

  
db = zSQLAlchemyBrick(model_class=Base)

if TYPE_CHECKING:
    BaseModel = db.make_declarative_base(Base)
else:
    BaseModel = db.Model