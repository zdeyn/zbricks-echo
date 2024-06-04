from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger

logger = zbricks_logger(__name__)

def call_handler(*arg_types):
    def decorator(func: Callable):
        # logger.debug(f"Registering call handler for {func} with arg_types: {arg_types}")
        if not hasattr(func, '_zbricks_handlers'):
            # logger.debug(f"Creating _zbricks_handlers attribute on {func}")
            setattr(func, '_zbricks_handlers', {})
        handlers : dict = getattr(func, '_zbricks_handlers')
        if 'call' not in handlers.keys():
            # logger.debug(f"Creating call handlers attribute on {func}")
            handlers['call'] = {}
        handlers['call'][arg_types] = func
        # logger.debug(f"Handlers: {handlers}")
        return func
    return decorator

class zCallableAugmentation:
    # _call_handlers: Dict[Tuple, Callable] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._register_call_handlers()

    @classmethod
    def __call__(cls, *data: Optional[Any]):
        handlers : Dict[str, Dict] = getattr(cls, '_zbricks_handlers', {})
        if not handlers['call']:
            raise NotImplementedError(f"{cls}: Not intended for use as a callable FROM AUGMENTATION")
        
        for arg_types, handler in handlers['call'].items():
            if len(arg_types) == 1 and isinstance(data, arg_types[0]):
                return handler(cls, data)
            elif isinstance(data, tuple) and len(data) == len(arg_types):
                if all(isinstance(d, t) for d, t in zip(data, arg_types)):
                    return handler(cls, *data)
                
        raise NotImplementedError(f"{cls}: No handlers registered for __call__ input ({type(data)}): |{data}|")

    @classmethod
    def _register_call_handlers(cls):
        
        if not hasattr(cls, '_zbricks_handlers'):
            setattr(cls, '_zbricks_handlers', {})
        handlers : dict = getattr(cls, '_zbricks_handlers')
        if not 'call' in handlers.keys():
            handlers['call'] = {}

        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):            
            method_handlers : dict = getattr(method, '_zbricks_handlers', {})
            if not 'call' in method_handlers.keys():
                method_handlers['call'] = {}
            
            handlers['call'].update(method_handlers['call'])

class zContextProxy:
    
    def push_local(self):
        pass

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

    _zbricks_handlers: Dict[str, Dict[Any, Any]]

    # def _post_init(self):
    #     '''
    #     Hook for subclasses to perform post-initialization tasks.
    #     '''
    #     pass

    def __init__(self, *args, **kwargs) -> None:
        '''
        Create an instance of `zBrick`, optionally with given name.

        :param name: The configuration of the brick.
        :type name: Optional[str]
        '''
        super().__init__(*args, **kwargs)
        # self._post_init()
        
    
    @classmethod
    def __call__(cls, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being callable.
        '''
        raise NotImplementedError(f"{cls}: Not intended for use as a callable FROM BASE CLASS")
    
    @classmethod
    def __iter__(cls) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being iteratable.
        '''
        raise NotImplementedError(f"{cls}: Not intended for use as an iterator")
    
    @classmethod
    def __next__(cls) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a generator.
        '''
        raise NotImplementedError(f"{cls}: Not intended for use as a generator")
    
    @classmethod
    def __enter__(cls) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (enter).
        '''
        raise NotImplementedError(f"{cls}: Not intended for use as a context manager (enter)")

    @classmethod
    def __exit__(cls, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (exit).
        '''
        raise NotImplementedError(f"{cls}: Not intended for use as a context manager (exit)")

