# flake8: noqa
from flask import Blueprint

api = Blueprint("api", __name__)
from .posts import *
from .urls import *
