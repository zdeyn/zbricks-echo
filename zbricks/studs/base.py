from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__) 

from ..base import zBase

class zStud(zBase):
    '''
    Base class for components which provide a single, specific functionality.
    A `zStud` "should" have no dependencies on other components, and "should" be able to be used in isolation.
    Ideally, a `zStud` "should" be usable as a mixin.
    
    By itself, zStud provides:
    -  default (`NotImplementedError`-raising) implementations for:
        - `__call__`,
        - `__iter__`,
        - `__next__`,         
        - `__enter__` and `__exit__` methods
    The above methods are intended to be overridden by subclasses to provide the desired functionality.
    '''      
    
    def __call__(self, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being callable.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable (zBrick)")
    
    def __iter__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being iteratable.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as an iterator (zBrick)")
    
    def __next__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a generator.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a generator (zBrick)")
    
    def __enter__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (enter).
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a context manager (enter) (zBrick)")

    def __exit__(self, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (exit).
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a context manager (exit) (zBrick)")


