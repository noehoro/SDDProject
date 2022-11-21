import json
from sqlalchemy.ext import mutable
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Linked SQLAlchemy to our Python Environment, this links the SQL querying databases to Python 
# (Not Part of our Class Designs, used for enviornment setup only so that we can use databases with Python 3)
db = SQLAlchemy() 

'''
Class Site is an interface that maps the Database Site to a Python Class model. The Interface contains the database
Attribues, as well as an operator override to handle debugged (prints and references in data). Table contains attributes:
  - id -> primary key
  - name -> name of site
  - users -> users who manage the site (pointer)
  - machines -> pointer to machines in Machine table in site
'''
class Site(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    users = db.relationship('User', backref='site_users', lazy='dynamic')
    machines = db.relationship('Machine', backref='site_machines', lazy='dynamic')

    def __repr__(self):
        return "<Site '{}'>".format(self.name)

'''
Class User is another database interface class, working similary to Site. It includes attributes:
   - id -> primary key
   - username -> self explanatory, is the username of a user
   - password -> password of a user (stored as a hash)
   - site -> name of site this user owns
'''
class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

'''
Class Machine, a database interface class, has the following attributes:
   - id -> primary key
   - time -> number representing (in seconds) how long a machine takes to finish
   - site -> Site the machine is a part of
   - broken -> flag that when True (1) signals a machine is broken and needs to be fixed 
'''
class Machine(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer())
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))
    broken = db.Column(db.Integer())

    def __repr__(self):
        return '<Machine {}>'.format(self.id)

'''
Class Activity, a database interface class, has the following attributes:
   - id -> primary key
   - time -> number represting the time a machine was started. This, when subtracted from current sys time
             tells how long a machine has been running for
   - site -> site the active machine is a part of
'''
class Activity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer())
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))

    def __repr__(self):
        return '<Machine {}>'.format(self.id)
