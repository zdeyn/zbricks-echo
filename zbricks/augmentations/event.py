from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from zbricks.studs import zDataStorageStud, zDataEntry
from zbricks.augmentations.base import zAugmentation
from zbricks.events import zEvent, zSampleEvent

@dataclass
class zSubscriptionEntry(zDataEntry):
    cls : Type[zEvent]

# TODO: Rewrite below as `zEventHandlerStud`, using `zDataStorageStud` and `zSubscriptionEntry`
# class zEventHandlerAugmentation(zAugmentation):
    # pass
    # _event_subscriptions: Dict[Callable, List[zEventSubscription]] = {}
    # _name: Optional[str] = None

    # def __init__(self, name: Optional[str] = None, **kwargs):
    #     if name is None:
    #         name = self.__class__.__name__
    #     self._name = name
    #     self._event_subscriptions = {}

    #     super().__init__(**kwargs)

    # @classmethod
    # def event_class_from_name(cls, name: str) -> Type:
    #     # TODO: This needs to be dynamic
    #     match name:
    #         case 'zEvent':
    #             return zEvent
    #         case 'zSampleEvent':
    #             return zSampleEvent
    #         case _:
    #             raise ValueError(f"Unknown event type: {name}")

    # def subscribe(self, f: Callable, sub_to: Optional[Type[zEvent]] = zEvent):
    #     if sub_to is None:
    #         sub_to = zEvent
    #     logger.debug(f"\nzEventDispatcher: Subscribing handler '{f}' to event type '{sub_to}'")
    #     if f not in self._event_subscriptions:
    #         self._event_subscriptions[f] = []
    #     subscription = zEventSubscription(sub_to)
    #     self._event_subscriptions[f].append(subscription)
    #     logger.debug(f"\nSubscriptions:")
    #     for handler, subscriptions in self._event_subscriptions.items():
    #         logger.debug(f"handler: '{handler}', subscriptions: '{subscriptions}'")
    #     logger.debug(f"\n")
    
    # def sub(self, *args):
    #     if len(args) == 1 and inspect.isclass(args[0]):
    #         event_type = args[0]
    #         def decorator(func):
    #             self.subscribe(func, event_type)
    #             return func
    #         return decorator
    #     else:
    #         func = args[0]
    #         self.subscribe(func)
    #         return func


    # @handler('call', type=zEvent)
    # def _handler(self, event: zEvent):
    #     replies = []
    #     logger.debug(f"\nzEventDispatcher: Sending event '{event}' to subscribers:")
    #     for handler, subscriptions in self._event_subscriptions.items():
    #         for subscription in subscriptions:
    #             if isinstance(event, subscription.cls):
    #                 logger.debug(f"\nzEventSubscription: Sending event '{event}' to handler '{handler}'")
    #                 reply = handler(event)
    #                 logger.debug(f"Got reply: '{reply}'")
    #                 replies.append(reply)

    #     logger.debug(f"Total replies '{replies}'")
    #     return replies
