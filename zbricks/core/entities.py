from dataclasses import dataclass
from .bases import Entity
from .types import Snowflake, Slug

@dataclass
class Permission(Entity):
    slug: Slug
    name: str = None

@dataclass
class Role(Entity):
    slug: Slug
    name: str = None

@dataclass
class User(Entity):
    discord_id: Snowflake = None