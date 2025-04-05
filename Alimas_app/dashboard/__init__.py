from flask import Blueprint

bp = Blueprint('dashboard', __name__)

from Alimas_app.dashboard import routes