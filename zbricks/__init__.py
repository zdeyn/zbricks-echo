"""
zBricks - a collection of bricks for building applications and tools.

An _application_ is an _assembly_ of _bricks_ which work together to provide a _system_.

A _brick_ is a _component_ that provides a _service_ or _functionality_. 
Bricks may be assembled in a variety of ways to solve a wide range of problems.

A brick exists within an automatically-generated set of named nested _contexts_ (being `root`, `parent`, and `local`).
Bricks may also attach a label/alias to their `local` context, so descendants/context partipants may locate the context by name.

Access to the Context is handled through a ContextProxy, which abstracts away the Context from the zBrick instances using it.

- Each zBrick creates a ContextProxy when instantiated.
- ContextProxy automatically locates or creates:
    - The shared/global Context ('root') - the top-level context
    - An enclosing Context ('parent') - shared by all siblings / children of direct-parent zBrick
    - A local Context ('local') - shared by all children of the current zBrick 

For the first zBrick created, the 'root', 'parent', and 'local' contexts are all the same.
"""

from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, Optional, Tuple, Union, Callable

from flask import Flask
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

from blinker import Namespace

from .logging import zbricks_logger
logger = zbricks_logger('zApp')

from .auth import zAuth
from .events import zEventDispatcher

class zBrick(ABC):
    name: Optional[str] = None

    def __init__(self, name = None):
        self.name = name or '(unnamed)'
        self._gen = self._generator()
        next(self._gen)  # Prime the generator
    
    def _generator(self) -> Generator[Any, Any, None]:
        while True:
            value = yield
            result = self._handler(value)
            yield result
    
    # @abstractmethod
    def _call_handler(self, *args) -> Any:
        # print(f"\n\nzBrick._call_handler called with args = '{args}'")
        # logger.debug(f"zBrick.__call__ called with args = '{args}'")
        arg = args[0] if args else None
        result = self._gen.send(arg)
        next(self._gen)  # Move to next yield
        return result

    @abstractmethod
    def _handler(self, inbound: Any) -> Any:
        ...

    def __call__(self, *args):
        result = self._call_handler(*args)
        return result
    
    def __iter__(self) -> Generator[Any, Any, None]:
        return self._gen


class zEchoBrick(zBrick):

    def _handler(self, *args) -> Any:
        return f"<zEchoBrick name='{self.name}'> received: '{args}'"

class zWsgiBrick(zBrick):
            
        def __init__(self, name=None):
            super().__init__(name)
            self.innerbrick = zEchoBrick(name='innerbrick')

        def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:  # type: ignore
            return super().__call__((environ, start_response))
        
        def _handler(self, inbound: Tuple) -> Iterable[bytes]:
            environ, start_response = inbound
            request = Request(environ)
            print(f"\n\nzWsgiBrick._handler called with request = '{request}'")
            response = self._handle_request(request)


            if isinstance(response, str):
                response = Response(response)
            elif isinstance(response, tuple):
                msg, status = response
                response = Response(msg, status)
            
            # start_response(response.status_code, response.headers)
            # return [response.data]
            return response(environ, start_response)
        
        def _handle_request(self, request: Request) -> Union[str, Tuple[str, str], Response]:
            # Implement your custom request handling logic here
            print(f"\n\nzWsgiBrick._handle_request called with request = '{request}'")
            msg = self.innerbrick(request.path)
            print(f"\n\ninnerbrick._handle_request returned,  msg = '{msg}'")
            code = 200
            print(f"\n\n-1---------------------------\n\n")

            # if request.path == '/':
            #     msg = "(index)"
            # elif request.path == '/hello':
            #     msg = "(hello)"
            # else:
            #     msg, code = f"404 path not found: {request.path}", 404
            if not msg.endswith('\n'):
                msg += '\n'
            msg += f"Brick name: {self.name}\nPath: {request.path}"
            print(f"\n\n-2---------------------------\n\n")
            response = Response(msg, code)
            print(f"\n\n-3---------------------------\n\n")
            print(f"\n\nzWsgiBrick._handle_request returning response = '{response}'")
            return response

class zApp(Flask):

    def __init__(self, import_name: str, config_class = None, **kwargs):

        logger.zbricks(f"Instantiating zApp, import_name = '{import_name}, config_class = '{config_class}")
        super().__init__(import_name, **kwargs)
        
        if config_class is not None:
            logger.debug(f"Configuring zApp")
            self.config.from_object(config_class)
        
        logger.zbricks(f"Instantiating zEventDispatcher, app = '{self}'")
        self._zevent = zEventDispatcher(self)
        self._event_namespace : Namespace|None = self._zevent.get_namespace()
        logger.zbricks(f"Finalized zEventDispatcher, namespace = '{self._event_namespace}'")

        logger.zbricks(f"Instantiating zAuth, app = '{self}'")
        self._zauth = zAuth(self)
        logger.zbricks(f"Finalized zAuth")

        logger.zbricks(f"Finalized zApp")

