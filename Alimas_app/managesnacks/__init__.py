from flask import Blueprint

bp = Blueprint('managesnacks', __name__)

from Alimas_app.managesnacks import routes