from flask import Blueprint

bp = Blueprint('managecustomers', __name__)

from Alimas_app.managecustomers import routes