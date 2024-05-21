import pytest
from unittest.mock import patch

from zbricks.core.zmachine import zMachine, zEvent

@pytest.mark.skip(reason="Event/signal handlers not yet implemented")
def test_no_event_handlers():
    pass
    # machine = zMachine()
    # some_event = machine.event()
    
    # results = some_event.send('i-am-sender', foo='bar')
    # assert results == []

@pytest.mark.skip(reason="Event/signal handlers not yet implemented")
def test_basic_handler():
    pass
    # machine = zMachine()
    # some_event = machine.event()

    # def qux(sender, **kwargs):
    #     # print('qux:', sender, kwargs)
    #     assert sender == 'i-am-sender'
    #     assert kwargs['foo'] == 'bar'
    #     return 'BINGO'
    
    # some_event._signal.connect(qux)
    
    # results = some_event.send('i-am-sender', foo='bar')

    # assert results == [(qux, 'BINGO')]

@pytest.mark.skip(reason="Event/signal handlers not yet implemented")
def test_decorator():
    pass
    # machine = zMachine()
    # some_event = machine.event()

    # # @some_event._signal.connect_via('i-am-sender')
    # @some_event.handle('i-am-sender')
    # def qux(sender, **kwargs):
    #     # print('qux:', sender, kwargs)
    #     assert sender == 'i-am-sender'
    #     assert kwargs['foo'] == 'bar'
    #     return 'BINGO'
    
    
    # results = some_event.send('i-am-sender', foo='bar')

    # assert results == [(qux, 'BINGO')]
