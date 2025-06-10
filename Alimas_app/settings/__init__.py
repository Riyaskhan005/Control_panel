from flask import Blueprint

bp = Blueprint('settings', __name__)

from Alimas_app.settings import routes