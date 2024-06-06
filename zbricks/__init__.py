"""
zBricks - a collection of bricks for building applications and tools.

An _application_ is an _assembly_ of _bricks_ which work together to provide a _system_.

A _brick_ is a _component_ that provides a _service_ or _functionality_. 
Bricks may be assembled in a variety of ways to solve a wide range of problems.

## Contexts

A brick exists within an automatically-generated set of named nested _contexts_ (being `root`, `parent`, and `local`).
Bricks may also attach a label/alias to their `local` context, so descendants/context partipants may locate the context by name.

Access to the Context is handled through a ContextProxy, which abstracts away the Context from the zBrick instances using it.

- Each zBrick creates a ContextProxy when instantiated.
- ContextProxy automatically locates or creates:
    - The shared/global Context ('root') - the top-level context
    - An enclosing Context ('parent') - shared by all siblings / children of direct-parent zBrick
    - A local Context ('local') - shared by all children of the current zBrick 

For the first zBrick created:
- 'root' is an alias/proxy to the global environment, until populated
- 'parent' is an alias/proxy to 'root', until populated
- 'local' is an alias/proxy to 'parent', until populated

## Other Stuff

zBricks can: 
- be part of a nested set of domains, the outermost of which is the root domain (usually owned by a zApplicationBrick)
- subscribe to and publish events (commands, queries, etc.)
- be attached to/owned by/own other bricks (connections)
- have configuration (`config`) that can be validated
- declare dependencies on abstracts/protocols for other bricks/external systems that must be fulfilled for the brick to function
- use the nested contexts and event dispatcher to locate and use the configured implementations for these abstract dependencies
"""

from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, Optional, Tuple, Union, Callable

from flask import Flask
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

# from blinker import Namespace

from .logging import zbricks_logger
logger = zbricks_logger('zApp')

# from .auth import zAuth
from .base import zBrick
from .augmentations import handler
# from .bricks import zEventDispatcher
from .events import zEvent, zSampleEvent, zRequestEvent