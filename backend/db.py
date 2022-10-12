from database import activity, machine, site, user
from flask_sqlalchemy import SQLAlchemy

class DB:

	def __init__(self, app):
		self.activity = SQLAlchemy().init(app)
		self.machine = SQLAlchemy().init(app)
		self.site = SQLAlchemy().init(app)
		self.user = SQLAlchemy().init(app)

