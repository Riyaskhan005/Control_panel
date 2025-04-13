from flask import Flask, render_template,request,jsonify
from Alimas_app.extensions import db
from Alimas_app.customersdue import bp
from Alimas_app.models.manage import CustomerEntry
from Alimas_app.utils.logwritter import LogWriter 
logger = LogWriter()


@bp.route('/')
def index():
    return render_template("customerdue.html")

