from typing import Any, Callable, Optional, Type
from werkzeug.wrappers import Request, Response
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
    request: Optional[Request] = None
