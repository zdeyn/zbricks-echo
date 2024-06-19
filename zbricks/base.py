from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Collection, Dict, List, Set, Type
from typing import Optional, TypeVar, Union

from rich import print

# Declare T to be a class type
T = TypeVar('T')

class zAttachableMixin:
    _name: Optional[str] = None
    _parent: Optional['zAttachableMixin'] = None
    _children: Set['zAttachableMixin']

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def parent(self) -> Optional['zAttachableMixin']:
        return self._parent

    @property
    def children(self) -> List['zAttachableMixin']:
        return [c for c in self._children]

    def __init__(self, 
                *args, 
                children: Optional[Union[Collection[Any], Dict[str, Any]]] = None, 
                name: Optional[str] = None,
                **kwargs
            ) -> None:
        # print(f"\nzAttachableMixin initialized with: {args}, {kwargs}, {children}, {name}")
        self.name = name or self.name
        self._children = set()
        children = kwargs.pop('children', children)

        if children:
            if isinstance(children, (list, set)):
                for a in children:                    
                    self.attach(a)
            elif isinstance(children, dict):
                for k, v in children.items():
                    self.attach(v, key = k)
            else:
                raise ValueError(f"Invalid attachments type: {type(children)}")
            
        
        super().__init__(*args, **kwargs)

    def attach(self, attachment: 'zAttachableMixin', key: Optional[str] = None) -> None:
        if not isinstance(attachment, zAttachableMixin):
            raise ValueError(f"Attachment is not zAttachable: {attachment}")
        if attachment.parent:
            raise ValueError(f"Attachment {attachment} already has a parent: {attachment.parent}")
        if attachment.name and attachment.name in self:
            raise KeyError(f"Key {attachment.name} already exists: {self[attachment.name]}")
        if key:
            if attachment.name:
                raise ValueError(f"Attachment {attachment} already has a key: {attachment.name}")
            attachment.name = key        

        self._children.add(attachment)
        attachment._parent = self

        if hasattr(self, '_attach_child'):
            self._attach_child(attachment)

        if hasattr(attachment, '_attach_parent'):
            attachment._attach_parent(self)
    
    # @abstractmethod
    # def _attach_child(self, child: 'zAttachableMixin') -> None:
    #     pass

    # @abstractmethod
    # def _attach_parent(self, parent: 'zAttachableMixin') -> None:
    #     pass

    def __getitem__(self, key: Union[str, Type[T]]) -> Union[Any, List[T]]:
        if isinstance(key, type):
            instances = [a for a in self.children if isinstance(a, key)]
            if instances:
                return instances
            raise KeyError(f"No instances of type {key} found")
        for attachment in self.children:
            if attachment._name == key:
                return attachment
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: str, brick: 'zAttachableMixin') -> None:
        if key in self:
            raise KeyError(f"Key {key} already exists")
        if brick.name and brick.name != key:
            raise ValueError(f"Brick {brick} already has a key: {brick.name}")
        brick.name = key        
        self.attach(brick)

    def __contains__(self, key: Union[str, type, object]) -> bool:
        key_match = any(child for child in self.children if child.name == key)
        if key_match: return True # early bail out

        instance_match = any(child for child in self.children if child is key)
        if instance_match: return True # early bail out

        type_match = isinstance(key, type) and any(issubclass(type(a), key) for a in self.children)
        return type_match