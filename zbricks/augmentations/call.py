from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from zbricks.studs import zDataStorageStud
from .base import zAugmentation, zAugmentationEntry

class zCallHandlerAugmentation(zAugmentation):

    def __call__(self, *data: Optional[Any]):
        aug_data : zDataStorageStud = getattr(self, '_aug_data', zDataStorageStud())
        entries : List[zAugmentationEntry] = [entry for entry in aug_data if entry.aug == 'call']
        
        if entries == []:
            raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable (zCallHandlerAugmentation)")
        
        handlers : List = []
        for entry in entries:
            sig = entry.kwargs.get('sig')
            if not isinstance(sig, tuple):
                sig = (sig,)
            if len(data) == len(sig):
                if all(isinstance(d, t) for d, t in zip(data, sig)):
                    handlers.append(entry.method)
        if handlers == []:
            raise NotImplementedError(f"{self.__class__}: No handlers registered for __call__ input ({type(data)}): |{data}|")
        
        replies = []
        for handler in handlers:
          replies.append(handler(*data))
        return replies


