from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union, get_type_hints
from typing import Generator, Callable, Dict, Tuple
import inspect

from zbricks.logging import zbricks_logger
logger = zbricks_logger(__name__) 

class zBase:    
    def _dump(self):
        """
        Output a self-analysis showing the hierarchy of the zBase instance and the source of its members.
        """
        print(f"## Instance Analysis: `<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>`")
        
        print("\n### Class Hierarchy:")
        for cls in inspect.getmro(self.__class__):
            if cls is not object:
                print(f" - `{cls.__name__}`")
        
        seen = {}
        skip = ('__doc__',)
        for cls in inspect.getmro(self.__class__):
            if cls is object:
                continue
            members = cls.__dict__.items()
            print(f"\nFrom {cls.__name__}:")
            for name, member in members:
                if name in skip: continue
                if name.startswith('__') and not name.endswith('__'):
                    continue
                if name in seen:
                    seen_name, seen_member = seen[name]
                    if seen_name == cls.__name__:
                        print(f"  - ~~`{name}` -> `{member}`~~")
                    else:
                        print(f"  - (~~`{cls.__name__}.{name}`~~) -> `{seen_name}` -> `{member}` ")
                else:
                    print(f"  - `{name}` = `{repr(member)}`")
                    seen[name] = (cls.__name__, member)
        
        # print("\nFrom object:")
        # for name, member in object.__dict__.items():
        #     if name in skip: continue
        #     if name in seen:
        #         original_class, original_member = seen[name]
        #         print(f"  - ~~`{name}` -> `{member}`~~")
        #     else:
        #         print(f"  - `{name}` -> `{member}`")


