from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger

logger = zbricks_logger(__name__)

def call_handler(*arg_types):
    """
    Decorator to register a call handler for a function.

    :param arg_types: The types of arguments the handler will accept.
    :type arg_types: Tuple

    :return: The decorated function.

    Installs a reference to arg_types in the _zbricks_func_handlers attribute of the decorated function.
    This is later used when constructing an instance of a class that has been decorated with zCallableAugmentation.

    func._zbricks_func_handlers = {
        'call': [arg_types, ...]
    }
    """
    def decorator(func: Callable):
        # logger.debug(f"Registering call handler for {func} with arg_types: {arg_types}")
        if not hasattr(func, '_zbricks_func_handlers'):
            # logger.debug(f"Creating _zbricks_func_handlers attribute on {func}")
            setattr(func, '_zbricks_func_handlers', {})
        handlers : dict = getattr(func, '_zbricks_func_handlers')
        if 'call' not in handlers.keys():
            # logger.debug(f"Creating call handlers attribute on {func}")
            handlers['call'] = []
        handlers['call'].append(arg_types)
        # logger.debug(f"Handlers: {handlers}")
        return func
    return decorator

class zCallableAugmentation:
    # _call_handlers: Dict[Tuple, Callable] = {}

    # def __init_subclass__(cls) -> None:
        # cls._register_call_handlers()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._install_call_handlers()

    # @classmethod
    def __call__(self, *data: Optional[Any]):
        instance_handlers : Dict[str, Dict] = getattr(self, '_zbricks_handlers', {})
        if not getattr(self, '_zbricks_handlers', None):
            raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable FROM AUGMENTATION")
        
        for arg_types, handlers in instance_handlers['call'].items():
            if len(arg_types) == 1 and isinstance(data, arg_types[0]):
                replies = []
                for handler in handlers:
                    replies.append(handler(data))                
                return replies[0]
            
            elif isinstance(data, tuple) and len(data) == len(arg_types):
                if all(isinstance(d, t) for d, t in zip(data, arg_types)):
                    replies = []
                    for handler in handlers:
                        replies.append(handler(*data))
                    return replies[0]
                
        raise NotImplementedError(f"{self.__class__}: No handlers registered for __call__ input ({type(data)}): |{data}|")

    # @classmethod
    # def _register_call_handlers(cls):
    #     pass
        # if not hasattr(cls, '_zbricks_class_handlers'):
        #     setattr(cls, '_zbricks_class_handlers', {})
        # class_handlers : dict = getattr(cls, '_zbricks_class_handlers')
        # if not 'call' in class_handlers.keys():
        #     class_handlers['call'] = {}        

        # for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):            
        #     method_handlers : dict = getattr(method, '_zbricks_func_handlers', {})
        #     if not 'call' in method_handlers.keys():
        #         method_handlers['call'] = {}

        #     for arg_types, _ in method_handlers['call'].items():
        #         print(f"\nFound: {arg_types} -> {name}")
        #         class_handlers['call'][arg_types] = class_handlers['call'].get(arg_types, [])
        #         class_handlers['call'][arg_types].append(name)
    
    def _install_call_handlers(self):
        instance_handlers : dict = getattr(self, '_zbricks_handlers', {})
        if not 'call' in instance_handlers.keys():
            instance_handlers['call'] = {}
        
        # print(f"\nInstalling call handlers for {self.__class__} into {self}")

        for name, method in inspect.getmembers(self):
            # print(f"\nChecking {name} for call handlers")
            if getattr(method, '_zbricks_func_handlers', None):
                # print(f"\nFound zbricks func handlers: {name}")
                method_handlers : dict = getattr(method, '_zbricks_func_handlers', {})
                method_handlers['call'] = method_handlers.get('call', [])
            
                for arg_types in method_handlers['call']:
                    # print(f"\nInstalling call handler: {arg_types} -> {name}")
                    instance_handlers['call'][arg_types] = instance_handlers['call'].get(arg_types, [])
                    instance_handlers['call'][arg_types].append(method)
                      

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


    def __init__(self, *args, **kwargs) -> None:
        '''
        Create an instance of `zBrick`, optionally with given name.

        :param name: The configuration of the brick.
        :type name: Optional[str]
        '''
        self._zbricks_handlers = {}
        super().__init__(*args, **kwargs)
        
    
    # @classmethod
    def __call__(self, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being callable.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable FROM BASE CLASS")
    
    # @classmethod
    def __iter__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being iteratable.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as an iterator")
    
    # @classmethod
    def __next__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a generator.
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a generator")
    
    # @classmethod
    def __enter__(self) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (enter).
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a context manager (enter)")

    # @classmethod
    def __exit__(self, *args) -> Generator[Any, Any, None]:
        '''
        Hook for subclasses to handle being a context manager (exit).
        '''
        raise NotImplementedError(f"{self.__class__}: Not intended for use as a context manager (exit)")

