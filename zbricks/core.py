from dataclasses import dataclass
from typing import Any, Collection, Dict, List, Optional, Set, Type, TypeVar, Union

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

class zBrick:
    _parent: Optional['zBrick'] = None
    _attachments: Set[_zAttachment]

    @property
    def parent(self) -> Optional['zBrick']:
        return self._parent
    
    @property
    def children(self) -> List['zBrick']:
        return [a.value for a in self._attachments if isinstance(a.value, zBrick)]

    def __init__(self, attachments: Optional[Union[Collection[Any], Dict[str, Any]]] = None) -> None:
        self._attachments = set()
        if attachments:
            if isinstance(attachments, dict):
                attachments = [_zAttachment(id=key, value=value) for key, value in attachments.items()]
            elif isinstance(attachments, (list, set)):
                attachments = [_zAttachment(id=None, value=value) for value in attachments]
            else:
                raise ValueError(f"Invalid attachments type: {type(attachments)}")
            for a in attachments:
                self._attach(a)            
    
    def _attach(self, attachment: _zAttachment) -> None:
        self._attachments.add(attachment)
        if isinstance(attachment.value, zBrick):
            if attachment.value._parent:
                raise ValueError(f"Attachment {attachment.value} already has a parent")
            attachment.value._parent = self

    def __getitem__(self, key: Union[str, Type[T]]) -> Union[Any, List[T]]:
        if isinstance(key, type):
            instances = [a.value for a in self._attachments if isinstance(a.value, key)]
            if instances:
                return instances
            raise KeyError(f"No instances of type {key} found")
        for attachment in self._attachments:
            if attachment.id == key:
                return attachment.value
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self:
            raise KeyError(f"Key {key} already exists")
        a = _zAttachment(id=key, value=value)
        self._attach(a)

    def __contains__(self, key: Union[str, type]) -> bool:
        key_match = any(key == a.id for a in self._attachments)
        if key_match: return True # early bail out

        instance_match = any(key is a.value for a in self._attachments)
        if instance_match: return True # early bail out

        type_match = isinstance(key, type) and any(issubclass(type(a.value), key) for a in self._attachments)
        return type_match
