# tests/helpers.py

from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

def create_request(method, path, data=None, cookies=None):
    # Configure an optional cookie for the header
    if cookies:
        headers = {'Cookie': cookies}
    else:
        headers = None

    builder = EnvironBuilder(method=method, path=path, json=data, headers=headers)
    env = builder.get_environ()
    return Request(env)