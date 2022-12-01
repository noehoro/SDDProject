import json
from sqlalchemy.ext import mutable
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Site(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    users = db.relationship('User', backref='site_users', lazy='dynamic')
    machines = db.relationship(
        'Machine', backref='site_machines', lazy='dynamic')

    def __repr__(self):
        return "<Site '{}'>".format(self.name)


class User(UserMixin, db.Model):
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
    activity = db.relationship(
        'Activity', backref='machine_activity', lazy='dynamic')

    def __repr__(self):
        return '<Machine {}>'.format(self.id)


class Activity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Integer())
    machine_id = db.Column(db.Integer(), db.ForeignKey('machine.id'))
    site = db.Column(db.Integer(), db.ForeignKey('site.id'))

    def __repr__(self):
        return '<Machine {}>'.format(self.id)
