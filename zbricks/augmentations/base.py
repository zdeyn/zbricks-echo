from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__)

from zbricks.studs import zDataStorageStud, zDataEntry

@dataclass
class zAugmentationEntry(zDataEntry):
    aug: str
    method: Callable
    args: Tuple
    kwargs: Dict

def handler(aug: str, *args, **kwargs):
    """
    Decorator to register augmentation data for a function.

    :param aug: The name that the augmentation data will be registered under.
    :type str:

    :param *args: The augmentation data to be registered.
    :type dict:

    :param **kwargs: The augmentation data to be registered.
    :type dict:

    :return: The decorated function.

    Appends `args` amd `kwargs` to `_zbricks_method_data[aug] = []`.
    This is later used by to install the data into `self._zbricks_data`.
    """

    logger.debug(f"`handler`: aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
    def decorator(method: Callable):
        logger.debug(f"Decorating '{method}', aug = '{aug}', args = '{args}', kwargs = '{kwargs}'")
        method_data : zDataStorageStud = getattr(method, '_zbricks_method_data', zDataStorageStud())
        entry = zAugmentationEntry(method=method, aug=aug, args=args, kwargs=kwargs)
        method_data.add(entry)
        setattr(method, '_zbricks_method_data', method_data)
        return method
    return decorator

class zAugmentation:
    # TODO: Placeholder, just in case
    pass