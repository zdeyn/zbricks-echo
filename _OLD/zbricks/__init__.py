from os import PathLike
from flask import Flask
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

from blinker import Namespace

from .logging import zbricks_logger
logger = zbricks_logger('zApp')

from .auth import zAuth
from .events import zEventDispatcher


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

