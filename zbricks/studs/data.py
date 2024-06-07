from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from .base import zStud

@dataclass
class zDataEntry:
    '''
    Dataclass for storing a single entry in a zDataStorageStud.
    '''
    pass

class zDataStorageStud(zStud):
    '''
    A registry for storing zDataEntry objects.
    '''
    _data: List[zDataEntry] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = []

    def add(self, entry: zDataEntry):
        if entry not in self._data:
            self._data.append(entry)
        else:
            raise ValueError(f"Entry already exists in registry: {entry}")
    
    def __iter__(self):
        return iter(self._data)