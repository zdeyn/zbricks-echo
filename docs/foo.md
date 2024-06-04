A `zBrick` may be used as a `Generator`.
- accepts `data:Any` via `self.send(data)`
- internally calls `self._parse_generator_input(data:Any)`
- checks registered handlers, e.g. `@gen_handler(variable_name = type, ...)`:
    - `@gen_handler(name_to_greet = str)` means 'call decorated method if `data` matches a single element, type `str`
    - `@gen_handler(foo = int, bar = str)` means 'call decorated method if `data` can be expanded into two elements matching `int` and `str`
    - `@gen_handler(environ = dict, start_response = Callable)` would set up a WSGI handler
    - ...
- if handler matching the signature is found, the handler is called with the variables expanded
- if no handler found, raises `NotImplementedError(f"{self}: I don't know how to handle this generator input ({type(data)}): |{data}|")

```python

base = zBrick() # create instance

reply = base.send('foo')
# NotImplementedError("<...>: I don't know to handle this generator input (str): |foo|)
from zbricks.zbrick import gen_handler
class zGreeterBrick(zBrick):
    @gen_handler(name_to_greet = str)
    def hello(self, name_to_greet:str = 'World'):
        return f"Hello, {name_to_greet}!"

greeter = zGreeterBrick()

reply = greeter.send('Joe')
# "Hello, Joe!"

reply = greeter.send(2)
# NotImplementedError("<...>: I don't know to handle this generator input (int): |2|)
```