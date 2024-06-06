from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger

logger = zbricks_logger(__name__)

def handler(aug: str, *args, **kwargs):
    """
    Decorator to register augmentation data for a function.

    :param aug: The name that the augmentation data will be registered under.
    :type str:

    :param argset: The augmentation data to be registered.
    :type dict:

    :return: The decorated function.

    Appends `argset` to `_zbricks_func_data[aug] = []`.
    This is later used by `zAugmentation` class to install the data into `self._zbricks_data`.

    func._zbricks_func_data = {
        aug: [argset, ...]
    }
    """
    logger.debug(f"`handler`: aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
    def decorator(func: Callable):
        logger.debug(f"Decorating '{func}', aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
        func_reg : zRegistry = getattr(func, '_zbricks_func_reg', zRegistry())
        entry = zRegistryEntry(method=func, aug=aug, args=args, kwargs=kwargs)
        func_reg.add(entry)
        setattr(func, '_zbricks_func_reg', func_reg)
        return func
    return decorator

@dataclass
class zRegistryEntry:
    method: Callable = field()
    aug: str = field()
    args: Tuple = field()
    kwargs: Dict[str, Any] = field()


class zAugmentation:
    _aug_registry : 'zRegistry'

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

class zRegistry():
    _data: List[zRegistryEntry] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = []

    def add(self, entry: zRegistryEntry):
        if entry not in self._data:
            self._data.append(entry)
        else:
            raise ValueError(f"Entry already exists in registry: {entry}")
    
    def __iter__(self):
        return iter(self._data)

class zCallableAugmentation(zAugmentation):

    def __call__(self, *data: Optional[Any]):
        aug_reg : zRegistry = getattr(self, '_aug_registry', zRegistry())
        entries = [entry for entry in aug_reg if entry.aug == 'call']
        
        if entries == []:
            raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable (zCallableAugmentation)")
        
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

class zBrick:
    '''
    Base class for all `zBrick`s. `zBrick`s are the building blocks of the `zbricks` framework.

   An _application_ is an _assembly_ of _bricks_ which work together to provide a _system_.

    A _brick_ provides a _service_ or _functionality_, each which may be assembled in a variety of ways to solve a range of problems.

    A brick exists within an automatically-generated set of named nested _contexts_ (being `root`, `parent`, and `local`).
    Bricks may attach an alias to their `local` context, so descendants/context partipants may locate the context by name.
    Bricks may publish themselves and/or their descendants to the 'local' context with a given alias.

    Access to the Context is handled through a ContextProxy, which abstracts away the Context from the zBrick instances using it.

    - Each zBrick creates a ContextProxy when instantiated.
    - ContextProxy automatically locates or creates:
        - The Root Context ('root') - the outer, top-level context (testing frameworks may supply a custom root context for isolation)
        - An enclosing Parent Context ('parent') - shared by all children of direct-parent zBrick (e.g 'all siblings')
        - A local Context ('local') - shared by all children of the current zBrick
    - ContextProxy also allows a brick to publish itself to the 'local' context with a given alias.

    For the first zBrick created, the 'root', 'parent', and 'local' contexts are each empty.

    zBricks can:
    
    - be part of a nested set of domains, the outermost of which is the root domain (usually owned by a zApplicationBrick)
    - subscribe to and publish events (commands, queries, etc.)
    - be attached to/owned by/own other bricks (connections)
    - have configuration (`config`) that can be validated
    - declare dependencies on abstracts/protocols for other bricks/external systems that must be fulfilled for the brick to function
    - use the nested contexts and event dispatcher to locate and use the configured implementations for these abstract dependencies
    '''

    _aug_registry : zRegistry

    def __init__(self, *args, **kwargs) -> None:
        '''
        Create an instance of `zBrick`, optionally with given name.

        :param name: The configuration of the brick.
        :type name: Optional[str]
        '''
        # self._aug_registry = getattr(self, '_aug_registry', zRegistry())
        super().__init__(*args, **kwargs)
        
    
    # @classmethod
    def __call__(self, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being callable.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable (zBrick)")
    
    # @classmethod
    def __iter__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being iteratable.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as an iterator (zBrick)")
    
    # @classmethod
    def __next__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a generator.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a generator (zBrick)")
    
    # @classmethod
    def __enter__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (enter).
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a context manager (enter) (zBrick)")

    # @classmethod
    def __exit__(self, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (exit).
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a context manager (exit) (zBrick)")

