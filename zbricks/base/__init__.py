from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
from zbricks.augmentations import handler, zCallHandlerAugmentation, zRegistry, zRegistryEntry

logger = zbricks_logger(__name__) 

class zBaseBrick:
    '''
    Base class for all `zBrick`s.
    
    By itself, zBrick provides:
    -  the capability to be augmented via the `@handler` decorator and zAugmentation classes,
    -  a `zRegistry` instance for storing augmentation data,
    -  a method for embedding augmentation data into new instances of the class,
    -  default (`NotImplementedError`-raising) implementations for:
        - `__call__`,
        - `__iter__`,
        - `__next__`,         
        - `__enter__` and `__exit__` methods
    The above methods are intended to be overridden by subclasses to provide the desired functionality.
    '''
    _aug_registry : zRegistry

    def __init__(self, **kwargs):
        self._aug_registry : zRegistry = zRegistry()
        super().__init__(**kwargs)
        self._embed_zbricks_data()
    
    def _embed_zbricks_data(self):     
        logger.debug(f"Embedding zBricks data, self = '{self}'")

        aug_reg : zRegistry = getattr(self, '_aug_registry', zRegistry())

        for name, method in inspect.getmembers(self):
            logger.debug(f"Checking {name} for zbricks_func_reg")

            func_reg : zRegistry = getattr(method, '_zbricks_func_reg', None)
            if not func_reg: continue

            for entry in func_reg:
                logger.debug(f"Found zbricks func data: name = '{name}', entry = '{entry}'")
                inst_entry = zRegistryEntry(method=method, aug=entry.aug, args=entry.args, kwargs=entry.kwargs)
                aug_reg.add(inst_entry)        
    
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

class zBrick(zCallHandlerAugmentation, zBaseBrick):
    '''
    Base class for all `zBrick`s.

    From `zBaseBrick`, `zBrick` provides:
    -  the capability to be augmented via the `@handler` decorator and zAugmentation classes,
    -  a `zRegistry` instance for storing augmentation data,
    -  a method for embedding augmentation data into new instances of the class,
    -  default (`NotImplementedError`-raising) implementations for:
        - `__iter__`,
        - `__next__`,         
        - `__enter__` and `__exit__` methods
    
    From `zCallableAugmentation`, `zBrick` provides:
    -  an implementation for `__call__`, which calls the appropriate handler based on augmentation data.
    '''
    pass

