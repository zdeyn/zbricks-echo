from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
from zbricks.events import zEvent, zSampleEvent

logger = zbricks_logger(__name__)

@dataclass
class zRegistryEntry:
    '''
    Dataclass for storing a single entry in a zRegistry.
    '''
    method: Callable = field()
    aug: str = field()
    args: Tuple = field()
    kwargs: Dict[str, Any] = field()

class zRegistry():
    '''
    A registry for storing zRegistryEntry objects.
    '''
    _data: List[zRegistryEntry] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = []

    def add(self, entry: zRegistryEntry):
        if entry not in self._data:
            self._data.append(entry)
        else:
            raise ValueError(f"Entry already exists in registry: {entry}")
    
    def __iter__(self):
        return iter(self._data)

def handler(aug: str, *args, **kwargs):
    """
    Decorator to register augmentation data for a function.

    :param aug: The name that the augmentation data will be registered under.
    :type str:

    :param argset: The augmentation data to be registered.
    :type dict:

    :return: The decorated function.

    Appends `argset` to `_zbricks_func_data[aug] = []`.
    This is later used by `zAugmentation` class to install the data into `self._zbricks_data`.

    func._zbricks_func_data = {
        aug: [argset, ...]
    }
    """
    logger.debug(f"`handler`: aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
    def decorator(func: Callable):
        logger.debug(f"Decorating '{func}', aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
        func_reg : zRegistry = getattr(func, '_zbricks_func_reg', zRegistry())
        entry = zRegistryEntry(method=func, aug=aug, args=args, kwargs=kwargs)
        func_reg.add(entry)
        setattr(func, '_zbricks_func_reg', func_reg)
        return func
    return decorator

class zAugmentation:
    # TODO: Placeholder, just in case
    pass

class zCallHandlerAugmentation(zAugmentation):

    def __call__(self, *data: Optional[Any]):
        aug_reg : zRegistry = getattr(self, '_aug_registry', zRegistry())
        entries = [entry for entry in aug_reg if entry.aug == 'call']
        
        if entries == []:
            raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable (zCallHandlerAugmentation)")
        
        handlers : List = []
        for entry in entries:
            sig = entry.kwargs.get('sig')
            if not isinstance(sig, tuple):
                sig = (sig,)
            if len(data) == len(sig):
                if all(isinstance(d, t) for d, t in zip(data, sig)):
                    handlers.append(entry.method)
        if handlers == []:
            raise NotImplementedError(f"{self.__class__}: No handlers registered for __call__ input ({type(data)}): |{data}|")
        
        replies = []
        for handler in handlers:
          replies.append(handler(*data))
        return replies


@dataclass
class zEventSubscription:
    cls : Type[zEvent]

class zEventHandlerAugmentation(zAugmentation):
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
    pass


# def handler(aug: str, *args, **kwargs):
#     """
#     Decorator to register augmentation data for a function.

#     :param aug: The name that the augmentation data will be registered under.
#     :type str:

#     :param argset: The augmentation data to be registered.
#     :type dict:

#     :return: The decorated function.

#     Appends `argset` to `_zbricks_func_data[aug] = []`.
#     This is later used by `zAugmentation` class to install the data into `self._zbricks_data`.

#     func._zbricks_func_data = {
#         aug: [argset, ...]
#     }
#     """
#     logger.debug(f"`handler`: aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
#     def decorator(func: Callable):
#         logger.debug(f"Decorating '{func}', aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
#         func_reg : zRegistry = getattr(func, '_zbricks_func_reg', zRegistry())
#         entry = zRegistryEntry(method=func, aug=aug, args=args, kwargs=kwargs)
#         func_reg.add(entry)
#         setattr(func, '_zbricks_func_reg', func_reg)
#         return func
#     return decorator


# class zAugmentation:
#     # TODO: Placeholder, just in case
#     pass

# class zCallHandlerAugmentation(zAugmentation):

#     def __call__(self, *data: Optional[Any]):
#         aug_reg : zRegistry = getattr(self, '_aug_registry', zRegistry())
#         entries = [entry for entry in aug_reg if entry.aug == 'call']
        
#         if entries == []:
#             raise NotImplementedError(f"{self.__class__}: Not intended for use as a callable (zCallHandlerAugmentation)")
        
#         handlers : List = []
#         for entry in entries:
#             sig = entry.kwargs.get('sig')
#             if not isinstance(sig, tuple):
#                 sig = (sig,)
#             if len(data) == len(sig):
#                 if all(isinstance(d, t) for d, t in zip(data, sig)):
#                     handlers.append(entry.method)
#         if handlers == []:
#             raise NotImplementedError(f"{self.__class__}: No handlers registered for __call__ input ({type(data)}): |{data}|")
        
#         replies = []
#         for handler in handlers:
#           replies.append(handler(*data))
#         return replies