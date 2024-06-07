from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from zbricks.studs import zStud, zDataStorageStud
from zbricks.augmentations import zCallHandlerAugmentation, zAugmentationEntry

class zBrick(zCallHandlerAugmentation, zStud):
    '''
    Base class for all `zBrick`s.

    `zBrick` provides:
    -  the capability to be augmented via the `@handler` decorator and zAugmentation classes,
    -  a `zRegistry` instance for storing augmentation data,
    -  a method for embedding augmentation data into new instances of the class,

    From `zCallableAugmentation`, `zBrick` provides:
    -  an implementation for `__call__`, which calls the appropriate handler based on augmentation data.
    
    From `zStud`, `zBrick` provides:
    -  default (`NotImplementedError`-raising) implementations for:
        - `__iter__`,
        - `__next__`,         
        - `__enter__` and `__exit__` methods
    
    
    '''    
    
    _aug_data : zDataStorageStud[zAugmentationEntry]

    def __init__(self, **kwargs):
        self._aug_data = zDataStorageStud()
        super().__init__(**kwargs)
        self._embed_zbricks_data()
    
    def _embed_zbricks_data(self):     
        logger.debug(f"Embedding zBricks data, self = '{self}'")

        aug_data = getattr(self, '_aug_data', zDataStorageStud())

        for name, method in inspect.getmembers(self):
            logger.debug(f"Checking {name} for zbricks_method_data")

            method_data : zDataStorageStud[zAugmentationEntry] = getattr(method, '_zbricks_method_data', None)
            if not method_data: continue

            for entry in method_data:
                logger.debug(f"Found zbricks method data: name = '{name}', entry = '{entry}'")
                inst_entry = zAugmentationEntry(method=method, aug=entry.aug, args=entry.args, kwargs=entry.kwargs)
                aug_data.add(inst_entry)


    