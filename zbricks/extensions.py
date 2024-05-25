from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
oauth = OAuth()
jwtm = JWTManager()
login_manager = LoginManager()