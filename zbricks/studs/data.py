from dataclasses import dataclass, field
from typing import TypeVar, Generic, List

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from .base import zStud

# Define a TypeVar for the zDataEntry type
T = TypeVar('T', bound='zDataEntry')

@dataclass
class zDataEntry:
    '''
    Dataclass for storing a single entry in a zDataStorageStud.
    '''
    pass

class zDataStorageStud(zStud, Generic[T]):
    '''
    A registry for storing zDataEntry objects.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data: List[T] = []

    def add(self, entry: T):
        if entry not in self._data:
            self._data.append(entry)
        else:
            raise ValueError(f"Entry already exists in registry: {entry}")
    
    def __iter__(self):
        return iter(self._data)
