from flask import Blueprint

bp = Blueprint('authentication', __name__)

from Alimas_app.Authentication import routes