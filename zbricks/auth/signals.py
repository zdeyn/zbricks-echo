import blinker

from blinker import Namespace
auth_signals = Namespace()

NEW_USER_CREATED = auth_signals.signal('new-user-created')
USER_REGISTERED = auth_signals.signal('user-registered')