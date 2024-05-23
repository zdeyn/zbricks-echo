# zbricks/core/events.py

from dataclasses import dataclass, field

import logging
from typing import Optional
logger = logging.getLogger('zbricks')
logger.setLevel(logging.INFO)  # Set minimum logging level


class zEvent:
    _handlers : list = []

    @classmethod
    def _reset(cls):
        cls._handlers = []

    @classmethod
    def fire(cls, *args, **kwargs):
        results = []
        logger.info(f"fire: cls={cls}, args={args}, kwargs={kwargs}")
        logger.info(f"fire: cls._handlers={cls._handlers}")

        for handler_cls, handler in cls._handlers:
            logger.info(f"fire: cls={handler_cls}, handler={handler}")

            for subscription_class, handler in cls._handlers:
                if issubclass(subscription_class, cls):
                    logger.info(f"fire: subscription_class={subscription_class}, handler={handler}")

                result = handler(*args, **kwargs)
                results.append( [(cls, handler, args, kwargs), result]) 
                logger.info(f"results={results}\n")

        return results
    
    @classmethod
    def connect(cls, handler):
        logger.info(f"connect: cls={cls}, handler={handler}")
        cls._handlers.append( (cls, handler) )


# decorator which configures the handler's subscription using zEvent.connect
def event(*event_args, **event_kwargs):
    logger.info(f"event: args = {event_args}, kwargs = {event_kwargs}")

    def decorator(handler):
        logger.info(f"decorator: handler = {handler}")

        def wrapper(*args, **kwargs):
            logger.info(f"wrapper: {handler}, args = {args}, kwargs = {kwargs}")
            return handler(*args, **kwargs)
        
        zEvent.connect(handler)
        return wrapper

    # Check if the decorator was called with arguments or not
    if len(event_args) == 1 and callable(event_args[0]):
        return decorator(event_args[0])
    else:
        return decorator