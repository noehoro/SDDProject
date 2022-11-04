from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

class Auth:

	def __init__(self, encr='bcrypt', dep='auto'):
		self.encryption_protocol = encr
		self.encryption_object = CryptContext(schemes=[encr], deprecated=dep)

	def hash_key(self, string):
		return self.encryption_object.hash(string)

	def verify_key(self, hash, string):
		return self.encryption_object.verify(string, hash)


