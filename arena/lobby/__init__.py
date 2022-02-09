from flask import Blueprint

lobby = Blueprint('lobby', __name__)

from . import routes, events