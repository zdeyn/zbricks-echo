from dataclasses import dataclass
from typing import Any, Collection, Dict, List, Set, Type
from typing import Optional, TypeVar, Union

# Declare T to be a class type
T = TypeVar('T')

@dataclass(frozen=True)
class _zAttachment:
    id: Optional[str] = None  # must be unique if set
    value: Any = None

    # _zAttachment instances are equal if their ids are both set and equal, 
    # otherwise, if their ids are None and their values are equal
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _zAttachment):
            if self.id is not None or other.id is not None:
                return self.id == other.id
            return self.value == other.value
        return False

    def __repr__(self) -> str:
        return f"_zAttachment(id={self.id}, value={self.value})"


class zAttachableMixin:
    _parent: Optional['zAttachableMixin'] = None
    _children: Set[_zAttachment]

    @property
    def parent(self) -> Optional['zAttachableMixin']:
        return self._parent

    @property
    def children(self) -> List['zAttachableMixin']:
        return [a.value for a in self._children if isinstance(a.value, zAttachableMixin)]

    def __init__(self, children: Optional[Union[Collection[Any], Dict[str, Any]]] = None) -> None:
        self._children = set()
        if children:
            if isinstance(children, dict):
                children = [_zAttachment(id=key, value=value) for key, value in children.items()]
            elif isinstance(children, (list, set)):
                children = [_zAttachment(id=None, value=value) for value in children]
            else:
                raise ValueError(f"Invalid attachments type: {type(children)}")
            for a in children:
                self._attach(a)

    def _attach(self, attachment: _zAttachment) -> None:
        self._children.add(attachment)
        if isinstance(attachment.value, zAttachableMixin):
            if attachment.value._parent:
                raise ValueError(f"Attachment {attachment.value} already has a parent")
            attachment.value._parent = self

    def __getitem__(self, key: Union[str, Type[T]]) -> Union[Any, List[T]]:
        if isinstance(key, type):
            instances = [a.value for a in self._children if isinstance(a.value, key)]
            if instances:
                return instances
            raise KeyError(f"No instances of type {key} found")
        for attachment in self._children:
            if attachment.id == key:
                return attachment.value
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self:
            raise KeyError(f"Key {key} already exists")
        a = _zAttachment(id=key, value=value)
        self._attach(a)

    def __contains__(self, key: Union[str, type]) -> bool:
        key_match = any(key == a.id for a in self._children)
        if key_match: return True # early bail out

        instance_match = any(key is a.value for a in self._children)
        if instance_match: return True # early bail out

        type_match = isinstance(key, type) and any(issubclass(type(a.value), key) for a in self._children)
        return type_match