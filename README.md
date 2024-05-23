# `zBricks` - `Flask` gets zdeyn'd

## What is it?

`zBricks` is a suite of powerful subclasses, extensions, blueprints, middleware, and mixins designed to turbocharge Flask with enhanced behaviors and interfaces. It's Flask, but more modular, more flexible, and more... _me_.

## _Why_ is it?

Because I (`zdeyn`) got tired of fighting with Flask's limitations. Instead of reinventing the wheel and creating a whole new framework (which would probably just end up being a crappier version of Flask anyway), I've decided to supercharge Flask itself. Thus, `zBricks` was born - a toolkit to make Flask do more, better, and faster.

## How shall it be?

**100% `Flask` / Pallets Compatible**

`zBricks` is not a fork of Flask; it's an extension, wrapper and mixin, all at once. While doing so, it's essentially a drop-in replacement. 

It builds on top of Flask, ensuring complete compatibility with the Flask ecosystem. Think of it as Flask on steroids – all the goodness of Flask, but with extra muscle and capabilities.

---

## `zApp`: The Heart of zBricks

At the core of `zBricks` is the `zApp` class. 

It inherits from Flask, and that's where the fun starts - from pre-flight configuration checks through to auto-wired pre-package starter kits, the boring stuff is gone and productivity is _right there, friction-free_.

## Features

- **Pre-Flight Configuration Check**: Ensures all necessary configurations are in place before your app starts running.
- **Hierarchical Signaling/Event System**: Advanced event handling to keep your application organized and responsive. `zSignal` and `zEvent` wrap `blinker.NamedSignal` for shenanigans, including subscriptions for `zAncestorEvent` being notified when `zChildEvent` is fired. The firing of a `zSignal` or `zEvent` results in a _sequence of replies_, which may be filtered. The replies may be interpreted and processed as desired.
- **Priority-based/Cascading Route Handling**: Why connect `'/product/<uuid:sku\>'` to just one end-point, when you can connect it to _a sequence of end-points, which can be filtered and evaluated before being used?_. `werkzeug.router` has never worked so hard, or been bent so far over backwards!
- **URI-to-Event Routing**: Speaking of poor `werkzeug.router`, now it's doing backflips! The previously-mentioned _sequence of replies_ from `zEvent` firings combines nicely with the _sequence of end-points_ our updated router supports.

## Extensions and Blueprints

`zBricks` comes with a set of ready-to-use extensions and blueprints that can be easily integrated into your `zApp`.

### `zAuth` = (`zAuthentication.zUser` + `zAuthorization.(zPermission, zRole)`)

An extension that brings both _authorization_ (via `authlib`) and _authentication_ (via custom RBAC-inspired `zUser`, `zPermission`, `zRole` relationships) capabilities to your app.

## Functional Interface

A consistent, namespaced functional interface that makes integrating `zBricks` components into your app a breeze.

### Example Usage

```python
# app.py

from typing import Union
from zbricks import zConfig, zRequest, zResponse  # Flask's `Request` and `Response` classes, in a hat
from zbricks.tools import create_app, load_config  # functional tools
from zbricks.app import zApp  # Flask's `Flask` class, with a nice new dress
from zbricks.app.events import zHandleRequest  # zHandleRequest is a zCommandEvent(zEvent)
from zbricks.auth import zAuth, zAuthenticatedRequest
from zbricks.auth.events import zRequestAuthenticated  # zRequestAuthenticated is a zStateChangedEvent(zEvent)
from zbricks.auth.tools import has_credentials, extract_credentials, satisfies_permission, request_factory
from zbricks.auth.models import zUser, zCredentials, zPermission  # frozen dataclasses

app: zApp = create_app(__name__)
auth: zAuth = app.connect_brick(zAuth)  # handles all internal wiring and configuration, where possible

# Middleware: "extract authentication details and attempt upgrade of zRequest to zAuthenticatedRequest"
@app.before(zHandleRequest)  # this handler shall be fired _prior_ to `zHandleRequest` being fired
def upgrade_request(request: zRequest) -> Union[zRequest, zAuthenticatedRequest]:
    """Middleware to upgrade a zRequest to a zAuthenticatedRequest if credentials are present."""
    if has_credentials(request):
        credentials = extract_credentials(request)
        previous_request = request
        request = request_factory(zAuthenticatedRequest, request)
        if request is not previous_request:  # state changed, notify everyone before return
            zRequestAuthenticated.fire('upgrade_request', request=request, previous_state=previous_request)
    return request

@app.map('/dashboard', event=zAuthenticatedRequest, filter=lambda req: satisfies_permission(req.user, zPermission('moderator')))
def moderator_dashboard(request: zAuthenticatedRequest) -> zResponse:
    """Handler for the moderator dashboard."""
    # Inject moderator tools, handle business logic, etc. here
    response = zResponse("Moderator Dashboard Content")
    return response

@app.map('/dashboard', event=zAuthenticatedRequest)
def user_dashboard(request: zAuthenticatedRequest) -> zResponse:
    """Handler for the user dashboard."""
    # Inject user tools, handle business logic, etc. here
    response = zResponse("User Dashboard Content")
    return response

@app.map('/dashboard', event=zRequest)
def anonymous_dashboard(request: zRequest) -> zResponse:
    """Handler for the anonymous dashboard."""
    # Present "No, you're not authenticated!" and "Here's how to become so..." details
    # rather than an 'unauthorized' HTTP status
    response = zResponse("Anonymous Dashboard Content - Please authenticate.")
    return response

if __name__ == '__main__':
    config: zConfig = load_config()
    config['AUTH_SECRET_KEY'] = 'supersecretkey'
    app.init(config)  # Perform internal initialization, blueprint init, etc.
    app.run()
```

## Getting Started

1. **Install `zBricks`**

```bash
pip install zbricks
```

2. **Create Your zApp**

Use the `create_app` factory function to create an instance of `zApp`.

```python
from zbricks import create_app

app = create_app(__name__)
```

3. **Add Extensions and Blueprints**

Integrate the provided extensions and blueprints as needed.

```python
from zbricks.auth import zAuth
auth: zAuth = app.connect_brick(zAuth)  # handles all internal wiring and configuration of blueprint, ready for `app.init()`
```

4. **Run Your Application**

Ensure all configurations are in place and run your application as usual.

```python
from zbricks import zConfig, load_config

if __name__ == '__main__':
    config: zConfig = load_config()
    config['AUTH_SECRET_KEY'] = 'supersecretkey'
    app.init(config)  # Perform internal initialization, blueprint init, etc.
    app.run()
```

## Conclusion

`zBricks` is designed to take your Flask applications to the next level. With enhanced functionality and seamless integration, it's the perfect companion for developers who love Flask but need a bit more power and flexibility. So go ahead, give Flask a boost, and get zdeyn'd with `zBricks`!
