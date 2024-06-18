import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from .base import zBase

class zDecorator(zBase):
    def __init__(self, *args, **kwargs):
        self.func = args[0]

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
