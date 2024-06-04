
```python
>>> import zbricks
>>> a = zbricks.zNullBrick('A')
>>> a._expose_to_context(a._get_context_by_alias('local', hello = lambda x = 'World': print(f"Hello, {x}!")))
>>> print( a._dump_context_tree() )
<Context ['global'] = ['_'](
    <Context ['parent', 'local'] = ['A'](
        'hello': <callable function ...>
    )>
)>
>>> print(a._get_context_by_alias('local') is a._get_context_by_alias('parent'))
True
>>> b = zbricks.zNullBrick('B')
<Context ['global'] = ['_'](
    <Context ['parent', 'local'] = ['B']()>
)>
>>> print(a._get_context_by_alias('global') is b._get_context_by_alias('global'))
True
>>> a += b
>>> print( b._dump_context_tree() )
<Context ['global'] = ['_'](    
    <Context ['parent'] = ['A'](
        'hello': <callable function ...>,
        <Context ['local'] = ['B']()>
    )>      
)>
>>> a._label_context('my-domain')
>>> print( a._dump_context_tree() )
<Context ['global'] = ['_'](    
    <Context ['my-domain', 'parent', 'local'] = ['A'](
        'hello': <callable function ...>,
    )>      
)>
>>> print(a._get_context_by_alias('my-domain') is a._get_context_by_alias('local'))
True
>>> print( b._dump_context_tree() )
<Context ['global'] = ['_'](    
    <Context ['my-domain', 'parent'] = ['A'](
        'hello': <callable function ...>,

    )>      
)>
<Context 'global'['__'](
    <Context ['_'](
        <Context 'my-domain', 'parent'['A'](
            'hello': <callable function ...>,
            <Context ['local'] = ['B']()>
        )>
    )>
)>
>>> print(b._get_context_by_alias('parent') is b._get_context_by_alias('my-domain'))
True
```