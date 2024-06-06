# tests/test_auth_routes.py
from typing import Any, Callable, Iterable, Tuple, Union
import pytest

from unittest.mock import MagicMock
from flask import Flask, make_response
from rich import print
# from flask.testing import FlaskClient
from pytest_mock import MockFixture

from zbricks.base import zBrick, handler
from zbricks.bricks import zWsgiApplication
from werkzeug.wrappers import Request, Response
from werkzeug.test import Client

class Test_zBrick_Dev:    
    pass    
