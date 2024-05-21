
# zBricks

## zRequestResponseMachine Prototype

This project is a prototype for the `zRequestResponseMachine`, which is part of the `zBricks` framework. The `zRequestResponseMachine` is designed to handle HTTP requests and generate appropriate responses, serving as a foundational component for building web applications using the `zBricks` framework.

## Installation

Clone the repository to your local machine:

```sh
git clone https://github.com/zdeyn/zbricks.git
```

Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage

To use the `zRequestResponseMachine`, you can define routes and their corresponding handlers using `@zRequestResponseMachine.route`, a decorator connecting a handler to an event - in this case, `zRouteEvent`, an instance of `zEvent`.

Here's an example:

```python
# go.py

from zbricks.machines import zRequestResponseMachine, Request, Response

app = zRequestResponseMachine()

@app.route('/')
def index(request: Request):
    return Response('Hello, World!', status=200, content_type='text/plain')

@app.error(404)
def foo(request: Request):
    return Response('Custom Not Found', status=404, content_type='text/plain')

if __name__ == '__main__':
    app.run(use_reloader=True)

```

Then, run the `zRequestResponseMachine`:

```sh
python go.py
```

You can now access the defined routes in your web browser or through HTTP requests.

## Testing

Testing the `zRequestResponseMachine` is straight-forward:

```python
# tests/test_request_response.py
import pytest

from zbricks.machines import zRequestResponseMachine, Request, Response

from .helpers import create_request # builds Request objects

def test_index(machine : zRequestResponseMachine):
    request = create_request('GET', '/')
    response = machine.handle_request(request)
    
    assert response.status_code == 200
    assert response.data == b'Hello, World!'
    assert response.content_type == 'text/plain'

def test_custom_not_found(machine : zRequestResponseMachine):
    
    request = create_request('GET', '/custom-does-not-exist')
    response = machine.handle_request(request)
    
    assert response.status_code == 404
    assert response.data == b'Custom Not Found Error: /custom-does-not-exist'
    assert response.content_type == 'text/plain'

```

