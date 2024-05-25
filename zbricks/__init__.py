from flask import Flask
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

_zapp_class = Flask
class zApp(_zapp_class): pass
