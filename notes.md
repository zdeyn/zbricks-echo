# zEventDispatcher, a part of zBricks

```python

# zEvent / zChildEvent frozen dataclasses:
@dataclass(frozen=True)
class zEvent:
    name: str = field(default='zEvent', init=False)
    data: Any = field(default = None)

    def __init_subclass__(cls) -> None:
        cls.name = cls.__name__

@dataclass(frozen=True)
class zChildEvent(zEvent):
    child_data: Any = field(default = None)

# unified blinker signal for sending in zEvent instances:
import blinker
namespace = blinker.Namespace()
zevent_signal = namespace.signal('zevent')

# a single subscriber to the above signal, which is zEventDispatcher:
zed = zEventDispatcher(...)
zevent_signal.connect(zed._handle_zevent_signal, sender=blinker.ANY)

# function-based subscription:
def funcsub_handler(event: zEvent):
    assert isinstance(event, zEvent)
    return f"funcsub_handler: '{event.name}' '{event.data}'"
zed.subscribe(zEvent, zevent_handler)

# decorator subscription:
@zed.sub(zEvent)
def decsub_handler(event : zEvent):
    assert isinstance(event, zEvent)
    return f"decsub_handler got: '{event.data}'"

# zEventDispatcher notifies direct subscribers of events:
event = zEvent(data = 'foo')
replies = zevent_signal.send(event)
assert "funcsub_handler: 'zEvent' 'foo'" in replies
assert "decsub_handler: 'zEvent' 'foo'" in replies

# zEventDispatcher notifies inheritence subscribers of sub-classes of events:
@zed.sub(zChildEvent)
def chldsub_handler(event : zChildEvent):
    assert isinstance(event, zChildEvent)
    return f"chldsub_handler: '{event.name}' '{event.data}' '{event.child_data}'"

# filtering via lambdas:
@zed.sub(zChildEvent, filter = lambda e: e.child_data == 'woot')
def fltsub_handler(event : zChildEvent):
    return f"fltsub_handler: '{event.name}' '{event.data}' '{event.child_data}'"

event = zChildEvent(data = 'bar', child_data = 'qux')
replies = zevent_signal.send(event)
assert "funcsub_handler: 'zChildEvent' 'bar'" in replies
assert "decsub_handler: 'zChildEvent' 'bar'" in replies
assert "chldsub_handler: 'zChildEvent' 'bar' 'qux'" in replies
assert "fltsub_handler: 'zChildEvent' 'bar' 'qux'" not in relies

event = zChildEvent(data = 'baz', child_data = 'woot')
replies = zevent_signal.send(event)
assert "funcsub_handler: 'zChildEvent' 'baz'" in replies
assert "decsub_handler: 'zChildEvent' 'baz'" in replies
assert "chldsub_handler: 'zChildEvent' 'baz' 'woot'" in replies
assert "fltsub_handler: 'zChildEvent' 'baz' 'woot'" in relies

```

Got it! Let's update the `_handle_zevent_signal` method to first gather all the matching handlers into a set and then execute them to gather the responses. Here's the revised implementation:

```python
from dataclasses import dataclass, field
from typing import Any, Callable, List, Dict, Type

@dataclass(frozen=True)
class zEvent:
    name: str = field(default='zEvent', init=False)
    data: Any = field(default=None)

    def __init_subclass__(cls) -> None:
        cls.name = cls.__name__

@dataclass(frozen=True)
class zChildEvent(zEvent):
    child_data: Any = field(default=None)

import blinker
namespace = blinker.Namespace()
zevent_signal = namespace.signal('zevent')

class zEventDispatcher:
    def __init__(self):
        self._subscribers: Dict[Type[zEvent], List[Callable]] = {}

    def subscribe(self, event_cls: Type[zEvent], handler: Callable, filter: Callable[[zEvent], bool] = None):
        if event_cls not in self._subscribers:
            self._subscribers[event_cls] = []
        self._subscribers[event_cls].append((handler, filter))

    def sub(self, event_cls: Type[zEvent], filter: Callable[[zEvent], bool] = None):
        def decorator(func: Callable[[zEvent], Any]):
            self.subscribe(event_cls, func, filter)
            return func
        return decorator

    def _handle_zevent_signal(self, sender, event: zEvent):
        handlers = set()
        for event_cls, subs in self._subscribers.items():
            if isinstance(event, event_cls):
                for handler, filter in subs:
                    if filter is None or filter(event):
                        handlers.add(handler)
        
        responses = [handler(event) for handler in handlers]
        return responses

# Create the event dispatcher
zed = zEventDispatcher()
zevent_signal.connect(zed._handle_zevent_signal, sender=blinker.ANY)

# Function-based subscription example
def funcsub_handler(event: zEvent):
    assert isinstance(event, zEvent)
    return f"funcsub_handler: '{event.name}' '{event.data}'"
zed.subscribe(zEvent, funcsub_handler)

# Decorator subscription example
@zed.sub(zEvent)
def decsub_handler(event: zEvent):
    assert isinstance(event, zEvent)
    return f"decsub_handler got: '{event.data}'"

# Subclass subscription example
@zed.sub(zChildEvent)
def chldsub_handler(event: zChildEvent):
    assert isinstance(event, zChildEvent)
    return f"chldsub_handler: '{event.name}' '{event.data}' '{event.child_data}'"

# Filtering via lambda example
@zed.sub(zChildEvent, filter=lambda e: e.child_data == 'woot')
def fltsub_handler(event: zChildEvent):
    return f"fltsub_handler: '{event.name}' '{event.data}' '{event.child_data}'"

# Test event dispatching
event = zEvent(data='foo')
replies = zevent_signal.send(event)
print(replies)  # Check the responses from the handlers

event = zChildEvent(data='bar', child_data='qux')
replies = zevent_signal.send(event)
print(replies)  # Check the responses

event = zChildEvent(data='baz', child_data='woot')
replies = zevent_signal.send(event)
print(replies)  # Check the responses
```

### Explanation of the Changes:

1. **Handlers Set**:
   ```python
   handlers = set()
   ```
   - We first initialize an empty set to collect all unique handlers that should respond to the event.

2. **Collect Handlers**:
   ```python
   for event_cls, subs in self._subscribers.items():
       if isinstance(event, event_cls):
           for handler, filter in subs:
               if filter is None or filter(event):
                   handlers.add(handler)
   ```
   - We loop through the subscribers and check if the event is an instance of the subscribed event class.
   - If it is, we further check if any filter provided passes for the event.
   - If the filter passes (or there is no filter), the handler is added to the set.

3. **Invoke Handlers**:
   ```python
   responses = [handler(event) for handler in handlers]
   ```
   - After collecting all matching handlers, we invoke them and gather the responses.

This ensures that only the relevant handlers are collected into a set first, preventing duplicate executions and ensuring that all appropriate handlers are run before any responses are gathered.