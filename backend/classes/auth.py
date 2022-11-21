from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

'''
Class Auth handles user hashing and application security. It makes use of CryptContext from passlib,
and uses the bcrypt protocol to work. Auth does not do anything else other than hash and decode strings.
For security reasons, this application instantiates Auth each time is needed, deleting any paper trail created
by a attribute declaration of auth in the stack.
'''
class Auth:

	# Setup encryption protocol. By default, use automatically updated BCRYPT protocol
	def __init__(self, encr='bcrypt', dep='auto'):
		self.encryption_protocol = encr
		self.encryption_object = CryptContext(schemes=[encr], deprecated=dep)

	# Hash key transforms strings into hashs
	def hash_key(self, string):
		return self.encryption_object.hash(string)

	# Verify Key checks unhashed strings against hashes to verify their integrity
	def verify_key(self, hash, string):
		return self.encryption_object.verify(string, hash)


