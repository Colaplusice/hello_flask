from flask import Blueprint

play = Blueprint('play', __name__)
from .views import *
