from flask import Flask, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from auth import Auth

login = Blueprint('login', __name__)


