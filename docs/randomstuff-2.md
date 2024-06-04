from dataclasses import dataclass, field
from typing import Callable, Type, Optional, Dict, List, Any
from uuid import UUID, uuid4



@dataclass
class zeEvent:
    _id : UUID = field(default_factory=uuid4)
    payload : Dict[str, Any] = field(default_factory=dict)

class zeExample(zeEvent):
    example_list : List = field(default_factory=list)

class zeSubExample(zeExample):
    sub_int : int = field(default_factory=int)

@dataclass
class HandlerMetadata:
    event_class: Optional[Type]  # None means any event
    property_filters: Optional[Dict[str, Any]]  # e.g., ("user.id", "==", 12) or ("post.modify-outrank", "in", "user.roles")
    custom_filters: Optional[List[Callable]]  # List of lambda functions


def catchall_handler(event):
    print("Catch-all handler called")

def class_handler(event):
    print("Class handler called")

def property_handler(event):
    print("Property handler called")

def custom_handler(event):
    print("Custom handler called")

handlers = {
    catchall_handler: HandlerMetadata(None, {}, [])
    class_handler: HandlerMetadata(SomeEventClass, {"user.id": 12}, [lambda e: e.user.active]),
    # handler_2: HandlerMetadata(None, {}, [lambda e: e.type == "special"]),
}