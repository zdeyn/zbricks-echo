from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Collection, Dict, List, Set, Type
from typing import Optional, TypeVar, Union

# Declare T to be a class type
T = TypeVar('T')

# @dataclass(frozen=True)
# class _zAttachment:
#     id: Optional[str] = None  # must be unique if set
#     value: Any = None

#     # _zAttachment instances are equal if their ids are both set and equal, 
#     # otherwise, if their ids are None and their values are equal
#     def __eq__(self, other: Any) -> bool:
#         if isinstance(other, _zAttachment):
#             if self.id is not None or other.id is not None:
#                 return self.id == other.id
#             return self.value == other.value
#         return False

#     def __repr__(self) -> str:
#         return f"_zAttachment(id={self.id}, value={self.value})"


class zAttachableMixin:
    _name: Optional[str] = None
    _parent: Optional['zAttachableMixin'] = None
    _children: Set['zAttachableMixin']

    @property
    def parent(self) -> Optional['zAttachableMixin']:
        return self._parent

    @property
    def children(self) -> List['zAttachableMixin']:
        return [c for c in self._children]

    def __init__(self, 
                children: Optional[Union[Collection[Any], Dict[str, Any]]] = None, 
                *args, 
                name: Optional[str] = None,
                **kwargs
            ) -> None:
        
        self._children = set()
        if children:
            if isinstance(children, (list, set)):
                for a in children:                    
                    self.attach(a)
            elif isinstance(children, dict):
                for k, v in children.items():
                    self.attach(v, key = k)
            else:
                raise ValueError(f"Invalid attachments type: {type(children)}")
            
        self._name = name or self._name

    def attach(self, attachment: 'zAttachableMixin', key: Optional[str] = None) -> None:
        if not isinstance(attachment, zAttachableMixin):
            raise ValueError(f"Invalid attachment: {attachment}")
        if attachment.parent:
            raise ValueError(f"Attachment {attachment} already has a parent")
        if attachment._name and attachment._name in self:
            raise KeyError(f"Key {attachment._name} already exists")
        if key:
            if attachment._name:
                raise ValueError(f"Attachment {attachment} already has a key")
            attachment._name = key        

        self._children.add(attachment)
        self._attach_child(attachment)

        attachment._parent = self
        attachment._attach_parent(self)
    
    @abstractmethod
    def _attach_child(self, child: 'zAttachableMixin') -> None:
        pass

    @abstractmethod
    def _attach_parent(self, parent: 'zAttachableMixin') -> None:
        pass

    def __getitem__(self, key: Union[str, Type[T]]) -> Union[Any, List[T]]:
        if isinstance(key, type):
            instances = [a for a in self._children if isinstance(a, key)]
            if instances:
                return instances
            raise KeyError(f"No instances of type {key} found")
        for attachment in self._children:
            if attachment._name == key:
                return attachment
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: str, brick: 'zAttachableMixin') -> None:
        if key in self:
            raise KeyError(f"Key {key} already exists")
        if brick._name and brick._name != key:
            raise ValueError(f"Brick {brick} already has a key: {brick._name}")
        brick._name = key        
        self.attach(brick)

    def __contains__(self, key: Union[str, type, object]) -> bool:
        key_match = any(child for child in self._children if child._name == key)
        if key_match: return True # early bail out

        instance_match = any(child for child in self._children if child is key)
        if instance_match: return True # early bail out

        type_match = isinstance(key, type) and any(issubclass(type(a), key) for a in self._children)
        return type_match