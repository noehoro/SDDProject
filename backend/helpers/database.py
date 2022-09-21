import json
from sqlalchemy.ext import mutable
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Site(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    users = db.relationship('User', backref='site', lazy='dynamic')
    machines = db.relationship('Machine', backref='site', lazy='dynamic')

    def __repr__(self):
        return "<Site '{}'>".format(self.name)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Machine(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer())
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))

    def __repr__(self):
        return '<Machine {}>'.format(self.id)

class Activity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer())
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))

    def __repr__(self):
        return '<Machine {}>'.format(self.id)
