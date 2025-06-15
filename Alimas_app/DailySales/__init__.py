from flask import Blueprint

bp = Blueprint('Dailysales', __name__)

from Alimas_app.DailySales import routes