import pytest
from unittest.mock import MagicMock

from blinker import Namespace, NamedSignal, Signal
from typing import Set, Dict
import inspect

import logging

"""
Note:
This entire thing is kinda scrapped, but left as a passing test for later reference.
"""

# Configure the logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.debug('hello')

class LoggedSet(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"Initialized with elements: {self}")

    def add(self, element):
        super().add(element)
        logger.info(f"Added element: {element}, Current Set: {self}")

    def remove(self, element):
        super().remove(element)
        logger.info(f"Removed element: {element}, Current Set: {self}")

    def discard(self, element):
        super().discard(element)
        logger.info(f"Discarded element: {element}, Current Set: {self}")

    def clear(self):
        super().clear()
        logger.info("Cleared all elements, Current Set is empty")

    def update(self, *args):
        super().update(*args)
        logger.info(f"Updated with elements: {args}, Current Set: {self}")

    def intersection_update(self, *args):
        super().intersection_update(*args)
        logger.info(f"Intersection updated with elements: {args}, Current Set: {self}")

    def difference_update(self, *args):
        super().difference_update(*args)
        logger.info(f"Difference updated with elements: {args}, Current Set: {self}")

    def symmetric_difference_update(self, *args):
        super().symmetric_difference_update(*args)
        logger.info(f"Symmetric difference updated with elements: {args}, Current Set: {self}")

    def pop(self):
        element = super().pop()
        logger.info(f"Popped element: {element}, Current Set: {self}")
        return element

    def __getitem__(self, element):
        if element in self:
            logger.info(f"Accessed element: {element}")
            return element
        else:
            logger.info(f"Element {element} not found in set")
            raise KeyError(f"Element {element} not found in set")

    def __contains__(self, element):
        result = super().__contains__(element)
        logger.info(f"Checked for element: {element}, Present: {result}")
        return result

    def __iter__(self):
        logger.info(f"Created an iterator, Current Set: {self}")
        return super().__iter__()

    def __len__(self):
        length = super().__len__()
        logger.info(f"Checked length, Current Set length: {length}")
        return length

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f"LoggedSet({super().__repr__()})"


class OLDTest_Signals:    
    def test_standard_propagation(self):
        ns = Namespace()

        base_signal = ns.signal('base-signal')

        received_signals = []

        def base_receiver(sender, **kwargs):
            current_method_name = inspect.currentframe().f_code.co_name
            received_signals.append(f"{sender} triggered {current_method_name}")

        with base_signal.connected_to(base_receiver):
            base_signal.send('test_sender')

        expected_signals = ["test_sender triggered base_receiver"]
        
        assert received_signals == expected_signals
    
    def test_set_class_injection(self, caplog):
        mock_set_class = LoggedSet
        Signal.set_class = mock_set_class

        ns = Namespace()
        base_signal = ns.signal('base-signal')

        received_signals = []

        def base_receiver(sender, **kwargs):
            current_method_name = inspect.currentframe().f_code.co_name
            received_signals.append(f"{sender} triggered {current_method_name}")

        with caplog.at_level(logging.INFO):
            with base_signal.connected_to(base_receiver):
                base_signal.send('test_sender')

        expected_signals = ["test_sender triggered base_receiver"]
        
        assert received_signals == expected_signals

        logs = [record.message for record in caplog.records]

        assert any("Initialized with elements" in message for message in logs)
        assert any("Added element" in message for message in logs)
