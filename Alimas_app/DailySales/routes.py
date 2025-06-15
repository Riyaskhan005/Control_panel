import json
from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.DailySales import bp
from Alimas_app.models.manage import CustomerEntry,SnackEntry
from Alimas_app.utils.common import get_current_utc
from Alimas_app.utils.logwritter import LogWriter 
from Alimas_app.utils.login_requried import login_required
logger = LogWriter()


@bp.route('/')
@login_required
def index():
    return render_template("dailysales.html")