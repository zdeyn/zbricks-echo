from typing import Any, Callable, Optional, Type
from flask import Flask, Request, Response, request
from blinker import ANY, Namespace
from dataclasses import dataclass, field

from rich import print

from ..logging import zbricks_logger
logger = zbricks_logger('zEvent')

@dataclass(frozen=True)
class zEvent:
    name: str = field(default='zEvent', init=False)
    data: Any = None

    def __init_subclass__(cls) -> None:
        logger.zevent(f"Instantiating zEvent subclass, cls = {cls}")
        cls.name = cls.__name__

@dataclass(frozen=True)
class zSampleEvent(zEvent):
    pass

@dataclass(frozen=True)
class zRequestEvent(zEvent):
    request: Request = field(default_factory=lambda: request)


class zEventDispatcher:
    _app : Optional[Flask] = None
    _namespace: Optional[Namespace] = None

    @classmethod
    def event_class_from_name(cls, name: str) -> Type:    
        match name:
            case 'zEvent':
                return zEvent
            case 'zSampleEvent':
                return zSampleEvent
            case _:
                raise ValueError(f"Unknown event type: {name}")

    def __init__(self, app: Optional[Flask]):
        logger.zext(f"Creating zEventDispatcher, app = '{app}'")

        if app is not None:
            logger.debug(f"Configuring zEventDispatcher")
            self.init_app(app)
        logger.zext(f"Finalized zEventDispatcher")

    def init_app(self, app: Flask):
        logger.zext(f"Configuring zEventDispatcher, app = '{app}'")

        self._app = app
        app.extensions['zevent'] = self

        logger.debug(f"Creating Namespace for zEventDispatcher")
        self._namespace = Namespace() 
        zev = self._namespace.signal('zevent')
        # zev.connect(self.default_zevent_handler, sender=ANY)
        zev.connect(self.sample_zrequestevent_handler, sender='zRequestEvent')

        logger.zext(f"Registering 'before_request' handler, app = '{app}'")
        @app.before_request
        def fire_request_event():
            logger.debug(f"Handling 'before_request' event")
            event = zRequestEvent(request = request)
            logger.debug(f"Sending event, event = '{event}'")
            replies = self.send_event(event)
            logger.debug(f"Replies = '{replies}'")
            if replies:
                _, reply = replies[0]
                
                logger.zevent(f"Returning, reply = '{reply}'")
                return reply
    
    def get_namespace(self) -> Namespace|None:
        logger.debug(f"Getting namespace from zEventDispatcher, namespace = '{self._namespace}'")
        return self._namespace
    
    def subscribe(self, event_cls: Type, handler: Callable, filter = None):
        ev_name = event_cls.name
        zev = self._namespace.signal('zevent') # type: ignore[union-attr]
        logger.zevent(f"Subscribing: zev = '{zev}', ev_name = '{ev_name}', handler = '{handler}', filter = '{filter}'")
        # logger.debug(f"Signal = '{zev}', sender = '{ev_name}'")
        zev.connect(handler, sender=ev_name)
    
    def send_event(self, event: zEvent):
        logger.zevent(f"Sending event '{event.name}': '{event}'")

        zev = self._namespace.signal('zevent') # type: ignore
        assert zev is not None, "Signal 'zevent' is not defined"
        replies = zev.send(event.name, event=event)
        logger.zevent(f"Replies = '{replies}'")
        return replies

    def sample_zrequestevent_handler(self, sender, event: zRequestEvent):
        msg = f"Handled by sample_zrequestevent_handler"
        logger.debug(f"sample_zrequestevent_handler, msg = '{msg}', sender = '{sender}', event = '{event}'")
        
        if event.request.path == '/handled-by-event':
            msg = f"Request path is '{event.request.path}'"
            logger.debug(msg)
            return Response(msg, status=200, content_type='text/plain')