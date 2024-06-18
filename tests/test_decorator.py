# tests/test_decorator.py
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union
import pytest

from unittest.mock import MagicMock
from rich import print
from pytest_mock import MockFixture
import inspect
from dataclasses import dataclass, field

# intentionally using formal style for this file
import zbricks

class Test_Decorator_Dev:
    

    class testdec(zbricks.zDecorator):
        log : List = []

        @dataclass
        class _LogEntry:
            note: str
            args: Tuple
            kwargs: dict

        def __init__(self, *args, **kwargs):
            log = getattr(self.__class__, 'log', [])
            log.append(self._LogEntry('__init__', args, kwargs))
            super().__init__(*args, **kwargs)
        
        def __call__(self, *args, **kwargs):
            log = getattr(self.__class__, 'log', [])
            log.append(self._LogEntry('__call__', args, kwargs))
            super().__call__(*args, **kwargs)
    
    def test_decorates_bare_function(self):
        """`zDecorator` decorates bare methods without arguments."""
        
        @self.testdec
        def _(): return True

        assert len(self.testdec.log) == 1
        assert self.testdec.log[0] is '1'
    
    def test_decorates_bare_function_args(self):
        """`zDecorator` decorates bare methods with arguments."""
        
        @self.testdec('wonk', 2)
        def _(): return True

        assert len(self.testdec.log) == 1
        assert self.testdec.log[0] is '1'

class Test_Decorator_Basics:    
    
    def test_decorator_class_exists(self):
        """The `zDecorator` class exists."""
        assert inspect.isclass(zbricks.zDecorator)
    
    def test_decorator_class_can_be_subclassed(self):
        """The `zDecorator` class can be subclassed as a decorator."""
        class foo(zbricks.zDecorator):
            pass

        assert inspect.isclass(foo)
