# models.py

import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db

# class DiscordProfile(db.Model):
#     __tablename__ = 'discord_profiles'

#     id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))    
#     username: Mapped[str] = mapped_column(String(100), index=True)
#     discriminator: Mapped[str] = mapped_column(String(4), nullable=True)
#     global_name: Mapped[str] = mapped_column(String(100), nullable=True)    
#     avatar: Mapped[str] = mapped_column(String(100), nullable=True)
#     email: Mapped[str] = mapped_column(String(100), index=True, nullable=True)

# class User(db.Model):
#     __tablename__ = 'users'

#     id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
#     username: Mapped[str] = mapped_column(String(100), index=True, nullable=False, unique=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=True)
#     email: Mapped[str] = mapped_column(String(100), nullable=True)
#     avatar: Mapped[str] = mapped_column(String(100), nullable=True)

#     discord_id: Mapped[str] = mapped_column(String(64), ForeignKey('discord_profiles.id'), unique=True, index=True)
#     discord_profile: Mapped[DiscordProfile] = relationship("DiscordProfile", backref="user", uselist=False)

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    discord_id: Mapped[str] = mapped_column(String(64), nullable = False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), index=True, nullable=False, unique=True)
    access_token: Mapped[str] = mapped_column(String(255), index=True, nullable = True)
    refresh_token: Mapped[str] = mapped_column(String(255), index=True, nullable = True)
    is_authenticated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'<User {self.username}>'
    
    def __str__(self):
        return f'<User {self.username}>'