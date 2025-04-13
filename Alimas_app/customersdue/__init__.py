from flask import Blueprint

bp = Blueprint('customersdue', __name__)

from Alimas_app.customersdue import routes