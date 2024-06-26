from typing import List
from ..base import zFlaskExtensionBrick
from flask import Flask, flash, redirect, render_template, request, url_for

from zbricks.bricks.sqla import Mapped, mapped_column
from flask import Flask, Blueprint
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from zbricks.bricks.flask.extensions.sqlalchemy import db, BaseModel

class zAuthenticationBrick(zFlaskExtensionBrick):
	_name = 'auth'
	_bp = None

	def __init__(self, *args, **kwargs):
		print(f"\nzAuthenticationBrick initialized with: {args}, {kwargs}")
		zFlaskExtensionBrick.__init__(self, *args, **kwargs)

	def _attach_extension(self, app: Flask) -> None:
		
		print(f"\nAttaching {self} to {app}")
		self._bp = Blueprint('auth', __name__)
		self._setup_routes(self._bp)
	
		app.register_blueprint(self._bp, url_prefix='/auth')
	
	def _setup_routes(self, bp):
		@bp.route('/hello-world')
		def hello_world():
			return 'Hello, World! (love, Auth)'
		
		@bp.route('/register', methods=('GET', 'POST'))
		def register():
			if request.method == 'POST':
				username = request.form['username']
				password = request.form['password']
				error = None

				if not username:
					error = 'Username is required.'
				elif not password:
					error = 'Password is required.'

				if error is None:
					try:
						# db.execute(
						#     "INSERT INTO user (username, password) VALUES (?, ?)",
						#     (username, generate_password_hash(password)),
						# )
						# db.commit()
						user = User(username=username)
						user.secrets.append(PasswordSecret(secret=password))
					except db.IntegrityError:
						error = f"User {username} is already registered."
					else:
						return redirect(url_for("auth.login"))

				flash(error)

			return render_template('auth/register.html')

auth = zAuthenticationBrick()

class IdBase(BaseModel):
	__abstract__ = True
	id: Mapped[int] = mapped_column(primary_key=True)

class User(IdBase):
	__tablename__ = "users"
	username: Mapped[str] = mapped_column(unique=True)
	secrets: Mapped[List["PasswordSecret"]] = relationship(back_populates="user")

	def __repr__(self):
		return f"<{self.__class__.__name__} id={self.id}, username={self.username}, len(secrets)={len(self.secrets)}>"

class PasswordSecret(IdBase):
	__tablename__ = "password_secrets"
	secret: Mapped[str] = mapped_column()
	
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	user: Mapped["User"] = relationship(back_populates="secrets")    

	def __repr__(self):
		return f"<{self.__class__.__name__} id={self.id}, secret={self.secret}, user_id={self.user_id}>"