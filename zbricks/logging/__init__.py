# custom_logger.py
import logging

ZBRICKS = 11
logging.addLevelName(ZBRICKS, 'ZBRICKS')

ZEVENT = 12
logging.addLevelName(ZEVENT, 'ZEVENT')

ZEXT = 13
logging.addLevelName(ZEXT, 'ZEXT')

ZAUTH = 15
logging.addLevelName(ZAUTH, 'ZAUTH')

def zbricks(self, message, *args, **kwargs):
    if self.isEnabledFor(ZBRICKS):
        self._log(ZBRICKS, message, args, **kwargs)

def zevent(self, message, *args, **kwargs):
    if self.isEnabledFor(ZEVENT):
        self._log(ZEVENT, message, args, **kwargs)

def zext(self, message, *args, **kwargs):
    if self.isEnabledFor(ZEXT):
        self._log(ZEXT, message, args, **kwargs)

def zauth(self, message, *args, **kwargs):
    if self.isEnabledFor(ZEXT):
        self._log(ZEXT, 'zAuth: ' + message, args, **kwargs)

logging.Logger.zbricks = zbricks # type: ignore[attr-defined]
logging.Logger.zevent = zevent # type: ignore[attr-defined]
logging.Logger.zext = zext # type: ignore[attr-defined]
logging.Logger.zauth = zauth # type: ignore[attr-defined]

def zbricks_logger(name: str):
    logger = logging.getLogger(name)
    # logger.setLevel(logging.DEBUG)  # Set the default logging level
    return logger
