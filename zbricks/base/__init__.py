from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

def call_handler(*arg_types):
    def decorator(func: Callable):
        func._call_handler_arg_types = arg_types # type: ignore
        return func
    return decorator

class zCallableAugmentation:
    _call_handlers: Dict[Tuple, Callable] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._register_call_handlers()

    @classmethod
    def __call__(cls, *data: Optional[Any]):
        if not cls._call_handlers:
            raise NotImplementedError(f"{cls}: Not intended for use as a callable")
        for arg_types, handler in cls._call_handlers.items():
            if len(arg_types) == 1 and isinstance(data, arg_types[0]):
                return handler(cls, data)
            elif isinstance(data, tuple) and len(data) == len(arg_types):
                if all(isinstance(d, t) for d, t in zip(data, arg_types)):
                    return handler(cls, *data)
        raise NotImplementedError(f"{cls}: No handlers registered for __call__ input ({type(data)}): |{data}|")

    @classmethod
    def _register_call_handlers(cls):
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if hasattr(method, '_call_handler_arg_types'):
                arg_types = method._call_handler_arg_types
                cls._call_handlers[arg_types] = method

class zContextProxy:
    
    def push_local(self):
        pass

class zBrick(ABC, zCallableAugmentation):
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

    name: Optional[str] = None
    _gen: Generator[Any, Any, None]
    _ctx: zContextProxy

    @abstractmethod # MUST be implemented by subclasses
    def _handler(self, args: Tuple) -> Any:
        pass

    def _post_init(self):
        '''
        Hook for subclasses to perform post-initialization tasks.
        '''
        pass

    def __init__(self, *args, **kwargs) -> None:
        '''
        Create an instance of `zBrick`, optionally with given name.

        :param name: The configuration of the brick.
        :type name: Optional[str]
        '''
        name = kwargs.pop('name', None)
        if name is not None:
            self.name = name

        # Init ContextProxy
        self._ctx = zContextProxy()

        self._gen = self._generator()
        next(self._gen)  # Prime the generator

        super().__init__(*args, **kwargs)

        self._post_init()

    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
      
    # def __call__(self, *args: Tuple):
    #     result = self._gen.send(args)
    #     next(self._gen)  # Move to next yield
    #     return result
    
    def __iter__(self) -> Generator[Any, Any, None]:
        return self._gen
    
    def _generator(self) -> Generator[Any, Any, None]:
        while True:
            value = yield
            result = self._handler(value)
            yield result

