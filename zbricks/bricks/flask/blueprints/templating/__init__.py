
from zbricks.bricks.flask.base import zFlaskBlueprintBrick

from flask import Flask
from flask import flash, redirect, render_template, url_for
from flask import request


class zTemplatingBrick(zFlaskBlueprintBrick):
	_name = 'auth'
	_bp = None

	def __init__(self, *args, **kwargs):
		print(f"\nzTemplatingBrick initialized with: {args}, {kwargs}")
		zFlaskBlueprintBrick.__init__(self, 'templating', *args, **kwargs)

	def _attach_blueprint(self, app: Flask) -> None:		
		print(f"\nAttaching {self} to {app}")

		self._setup_routes()
	
		app.register_blueprint(self, url_prefix='/templating')
	
	def _setup_routes(self):
		@self.route('/hello-world-templating')
		def hello_world():
			return 'Hello, World! (love, Templating)'

templating = zTemplatingBrick()