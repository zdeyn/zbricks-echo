## Instance Analysis: `<zbricks.base.zBrick object at 0x7feae8e78d70>`

### Class Hierarchy:
 - `zBrick`
 - `zCallHandlerAugmentation`
 - `zAugmentation`
 - `zStud`
 - `zBase`

From zBrick:
  - `__module__` = `'zbricks.base'`
  - `__annotations__` = `{'_aug_registry': <class 'zbricks.augmentations.zRegistry'>}`
  - `__init__` = `<function zBrick.__init__ at 0x7feae81ffd80>`
  - `_embed_zbricks_data` = `<function zBrick._embed_zbricks_data at 0x7feae81ffe20>`

From zCallHandlerAugmentation:
  - (~~`zCallHandlerAugmentation.__module__`~~) -> `zBrick` -> `zbricks.augmentations` 
  - `__call__` = `<function zCallHandlerAugmentation.__call__ at 0x7feae81ff6a0>`

From zAugmentation:
  - (~~`zAugmentation.__module__`~~) -> `zBrick` -> `zbricks.augmentations` 
  - `__dict__` = `<attribute '__dict__' of 'zAugmentation' objects>`
  - `__weakref__` = `<attribute '__weakref__' of 'zAugmentation' objects>`

From zStud:
  - (~~`zStud.__module__`~~) -> `zBrick` -> `zbricks.base` 
  - (~~`zStud.__call__`~~) -> `zCallHandlerAugmentation` -> `<function zStud.__call__ at 0x7feae81ff600>` 
  - `__iter__` = `<function zStud.__iter__ at 0x7feae81ffa60>`
  - `__next__` = `<function zStud.__next__ at 0x7feae81ffb00>`
  - `__enter__` = `<function zStud.__enter__ at 0x7feae81ffba0>`
  - `__exit__` = `<function zStud.__exit__ at 0x7feae81ffc40>`

From zBase:
  - (~~`zBase.__module__`~~) -> `zBrick` -> `zbricks.base` 
  - `_dump` = `<function zBase._dump at 0x7feae8dafce0>`
  - (~~`zBase.__dict__`~~) -> `zAugmentation` -> `<attribute '__dict__' of 'zBase' objects>` 
  - (~~`zBase.__weakref__`~~) -> `zAugmentation` -> `<attribute '__weakref__' of 'zBase' objects>` 
